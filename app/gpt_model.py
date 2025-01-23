from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class GPTModel:
    def __init__(self, model_name: str):
        print("Descargando modelo. Esto podría tardar un poco la primera vez...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
        print("Modelo GPT2 descargado y cargado en memoria.")

    def generate_text(self, prompt: str, max_length: int, temperature: float, top_p: float):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return generated_text