from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

# Load the model and tokenizer from the local directory
model_path = "./model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Ensure the model is in evaluation mode
model.eval()

@app.post("/generate/")
async def generate_text(prompt: str, max_length: int = 512):
    try:
        # Tokenize the input prompt
        inputs = tokenizer(prompt, return_tensors="pt")

        # Generate the response with the specified max_length
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                pad_token_id=tokenizer.eos_token_id,
                temperature=0.7,  # Adjust temperature for more creative responses
                top_k=50,         # Adjust top_k for more diverse responses
                top_p=0.95        # Adjust top_p for more diverse responses
            )

        # Decode the generated tokens to text
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
