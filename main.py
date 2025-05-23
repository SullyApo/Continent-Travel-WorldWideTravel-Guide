from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes
from app.api import auth, chat
from app.api.destinations import router as destinations_router
from app.api.hebergements import router as hebergements_router
from app.api.voyages import router as voyages_router

# Configuration
from app.core.config import settings
from app.db.database import init_db
from app.utils.logging import logger
from prometheus_fastapi_instrumentator import Instrumentator

# Correction 1 : Création de l'app APRÈS les imports
app = FastAPI(
    title="Chatbot API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None  # Désactive Redoc si non utilisé
)

# Correction 2 : Instrumentation Prometheus AVANT les middlewares
Instrumentator().instrument(app).expose(app)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, "CORS_ORIGINS") else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True  # Nouveau : Pour les cookies/auth
)

# Routeurs (Correction 3 : Prefix cohérent pour voyages)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/chat", tags=["Chatbot"])
app.include_router(destinations_router, prefix="/api/destinations", tags=["Destinations"])
app.include_router(hebergements_router, prefix="/api/hebergements", tags=["Accommodations"])
app.include_router(voyages_router, prefix="/api/voyages", tags=["Voyages"])  # Prefix ajouté

# Événements startup/shutdown (Correction 4 : Ajout de shutdown)
@app.on_event("startup")
async def on_startup():
    logger.info("Initialisation de la base de données...")
    await init_db()
    logger.info(f"Environnement: {settings.ENV}")  # Debug utile

@app.on_event("shutdown")  # Nouveau
async def on_shutdown():
    logger.warning("Arrêt du serveur en cours...")

# Point de santé (Nouveau : Requis pour Kubernetes/Docker)
@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Démarrage du serveur sur {settings.BACKEND_HOST}:{settings.BACKEND_PORT}")
    uvicorn.run(
        app,
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        log_config=None,
        reload=settings.ENV == "dev"  # Auto-reload en dev uniquement
    )