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

    def load_model(self):
        """Carrega o modelo e o tokenizer."""
        if not self.model:
            print("Carregando modelo DeepSeek...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float32,
                device_map="auto",
                low_cpu_mem_usage=True,
                offload_folder="./offload",  # ← Adicione esta linha
                # load_in_4bit=True  # ← Ative quantização 4-bit (opcional)
            )
            print("Modelo carregado com sucesso!")

    def generate_response(self, prompt):
        """Gera uma resposta com base no prompt."""
        self.load_model()
        
        # Configuração do tokenizer
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token  # Define pad_token
        
        # Tokenização com atenção a padding
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to("cpu")  # Use "cuda" se tiver GPU
        
        # Geração com parâmetros seguros
        outputs = self.model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,  # Adiciona máscara de atenção
            max_new_tokens=200,  # Reduza para melhor performance
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id  # Define explicitamente
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)