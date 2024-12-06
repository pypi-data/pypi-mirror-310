from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Yukti:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.model.eval()

    def generate_text(self, prompt, max_length=512):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0.7,
                top_k=50,
                top_p=0.95
            )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
