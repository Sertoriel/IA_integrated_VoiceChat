import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv

load_dotenv()

class DeepSeekLocal:
    def __init__(self):
        self.model_path = os.getenv("DEEPSEEK_MODEL_PATH", "./models/deepseek-local")
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Usando dispositivo: {self.device.upper()}")

    def load_model(self):
        """Carrega o modelo e o tokenizer."""
        if not self.model:
            print("Carregando modelo DeepSeek...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            # Configuração dinâmica para GPU/CPU
            load_params = {
                "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
                "low_cpu_mem_usage": True,
                "offload_folder": "./offload"
            }
            
            if self.device == "cuda":
                load_params["device_map"] = "auto"
            else:
                load_params["device_map"] = "cpu"
                load_params["offload_state_dict"] = True

            # Para quantização 4-bit (descomente se necessário)
            # load_params["load_in_4bit"] = True
            # load_params["bnb_4bit_compute_dtype"] = torch.float16

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                **load_params
            )
            
            if self.device == "cuda":
                self.model = self.model.to(self.device)
                
            print("Modelo carregado com sucesso!")

    def generate_response(self, prompt):
        """Gera uma resposta com base no prompt."""
        self.load_model()
        
        # Configuração do tokenizer
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Tokenização com atenção ao dispositivo
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        
        # Geração adaptativa
        try:
            outputs = self.model.generate(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        except RuntimeError as e:
            return f"Erro na geração: {str(e)}"