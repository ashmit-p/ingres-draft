import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LANGCHAIN_TRACING: bool = os.getenv("LANGCHAIN_TRACING", "false").lower() == "true"

settings = Settings()
