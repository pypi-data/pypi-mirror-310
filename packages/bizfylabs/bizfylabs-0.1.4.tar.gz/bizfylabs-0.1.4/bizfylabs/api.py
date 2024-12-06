import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# URL of the server-side API
server_url = "http://88.222.241.88:8000/generate/"

@app.post("/generate/")
async def generate_text(prompt: str, max_length: int = 512):
    try:
        response = requests.post(server_url, json={"prompt": prompt, "max_length": max_length})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_text_from_server(prompt: str, max_length: int = 512):
    try:
        response = requests.post(server_url, json={"prompt": prompt, "max_length": max_length})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
