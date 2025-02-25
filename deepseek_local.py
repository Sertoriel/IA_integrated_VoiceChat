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
                torch_dtype=torch.float16,
                device_map="auto"
            )
            print("Modelo carregado com sucesso!")

    def generate_response(self, prompt):
        """Gera uma resposta com base no prompt."""
        self.load_model()
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=1500,
            temperature=0.7,
            do_sample=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)