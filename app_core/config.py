from typing import Optional
import os
from pydantic import BaseSettings, validator, AnyUrl
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Configuration Database
    DB_URL: Optional[str] = os.getenv(
        "DB_URL", 
        "postgresql+asyncpg://postgres:postgres@localhost:5432/chatbot"
    )
    
    # Sécurité
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # RASA Configuration
    RASA_HTTP_URL: str = os.getenv(
        "RASA_HTTP_URL", 
        "http://rasa:5005/webhooks/rest/webhook"
    )
    RASA_ACTION_ENDPOINT: str = os.getenv(
        "RASA_ACTION_ENDPOINT",
        "http://rasa:5055/webhook"
    )
    
    # Redis
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://:${REDIS_PASSWORD}@redis:6379/0"
    )
    
    # External APIs
    AVIATIONSTACK_API_URL: str = os.getenv("AVIATIONSTACK_API_URL", "http://api.aviationstack.com/v1")
    AVIATIONSTACK_API_KEY: str = os.getenv("AVIATIONSTACK_API_KEY", "")
    
    BOOKING_API_URL: str = os.getenv(
        "BOOKING_API_URL",
        "https://booking-api.example.com/v1"
    )
    BOOKING_API_KEY: str = os.getenv("BOOKING_API_KEY", "")
    
    # Validation
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:  # Augmenté à 32 caractères pour plus de sécurité
            raise ValueError("La clé secrète doit faire au moins 32 caractères")
        return v
        
    @validator("DB_URL")
    def validate_db_url(cls, v):
        if "postgresql+asyncpg" not in v and "sqlite+aiosqlite" not in v:
            raise ValueError("URL de base de données non supportée")
        return v

settings = Settings()