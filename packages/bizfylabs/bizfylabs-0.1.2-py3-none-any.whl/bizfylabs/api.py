from fastapi import FastAPI, HTTPException
from .model import Yukti

app = FastAPI()

# Initialize the model
model_path = "./model"
yukti_model = Yukti(model_path)

@app.post("/generate/")
async def generate_text(prompt: str, max_length: int = 512):
    try:
        response = yukti_model.generate_text(prompt, max_length)
        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
