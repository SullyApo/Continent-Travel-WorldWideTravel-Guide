import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Fichier de logs avec rotation
handler = RotatingFileHandler(
    "app.log", maxBytes=5*1024*1024, backupCount=3  # 5MB par fichier
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)