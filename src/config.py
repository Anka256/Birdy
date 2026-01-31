import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "qwen3:8b")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0))
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")

    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    XENOCANTO_API_KEY = os.getenv("XENOCANTO_API_KEY")
    
    INATURALIST_PHOTO_LIMIT = int(os.getenv("INATURALIST_PHOTO_LIMIT", 15))
    XENOCANTO_SOUND_LIMIT = int(os.getenv("XENOCANTO_SOUND_LIMIT", 5))

config = Config()
