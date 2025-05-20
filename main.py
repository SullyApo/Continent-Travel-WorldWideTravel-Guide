from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes
from app.api import auth, chat
from app.api.destinations import router as destinations_router
from app.api.hebergements import router as hebergements_router

# Configuration
from app.core.config import settings
from app.db.database import init_db
from app.utils.logging import logger  # Import direct du logger

app = FastAPI(
    title="Chatbot API",
    version="1.0.0",
    docs_url="/docs"  # Optionnel : personnalisation de l'URL de documentation
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, "CORS_ORIGINS") else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routeurs
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/chat", tags=["Chatbot"])
app.include_router(destinations_router, prefix="/api/destinations", tags=["Destinations"])
app.include_router(hebergements_router, prefix="/api/hebergements", tags=["Accommodations"])

@app.on_event("startup")
async def on_startup():
    logger.info("Initialisation de la base de données...")
    await init_db()
    logger.info("Prêt à recevoir des requêtes")

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Démarrage du serveur sur {settings.BACKEND_HOST}:{settings.BACKEND_PORT}")
    uvicorn.run(
        app,
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        log_config=None  # Désactive les logs par défaut d'uvicorn
    )