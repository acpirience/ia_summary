import sys

from loguru import logger


def setup_logging():
    logger.remove()

    logger.add(
        sys.stdout,
        level="INFO",  # Filtrage : INFO et supérieur à l'écran
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        enqueue=True,  # Thread-safe et asynchrone
    )

    logger.add(
        "app_{time:YYYY-MM-DD}.log",  # Le nom du fichier inclut la date
        level="INFO",  # On garde tout (DEBUG+) dans le fichier
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}",
        encoding="utf-8",
        retention="5 days",  # Nettoie automatiquement les vieux fichiers après 10 jours
        enqueue=True,
    )
