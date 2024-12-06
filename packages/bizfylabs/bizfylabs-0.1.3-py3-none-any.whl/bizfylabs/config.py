import os

# Model configuration
MODEL_PATH = os.getenv("MODEL_PATH", "./model")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
