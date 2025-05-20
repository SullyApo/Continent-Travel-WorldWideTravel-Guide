from typing import Optional
import os
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URL: Optional[str] = os.getenv("DB_URL", "sqlite+aiosqlite:///./chatbot.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-par-defaut")
    RASA_URL: str = os.getenv("RASA_HTTP_URL", "http://localhost:5005/webhooks/rest/webhook")
    ALGORITHM: str = "HS256"  # Pour JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AVIATIONSTACK_API_URL: str = os.getenv("AVIATIONSTACK_API_URL", "http://api.aviationstack.com/v1")
    AVIATIONSTACK_API_KEY: str = os.getenv("AVIATIONSTACK_API_KEY", "")
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 16:
            raise ValueError("La clé secrète doit faire au moins 16 caractères")
        return v
    

settings = Settings()