# src/utils/config.py
import os

class Config:
    # --- LLM Settings ---
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    MISTRAL_MODEL_NAME = os.getenv("MISTRAL_MODEL_NAME", "mistral")

    # --- Logging Settings ---
    LOG_FILE = "logs/execution.log"
    LOG_LEVEL = "INFO"

# Create a single instance to be imported by other modules
config = Config()