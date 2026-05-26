import sys

from dotenv import dotenv_values
from loguru import logger

# Load .env
config: dict[str, str | None] = dotenv_values(".env")


# --- EMAIL CONFIGURATION ---
IMAP_SERVER = "imap.gmail.com"

EMAIL_USER: str | None = config["EMAIL_USER"]
EMAIL_PASSWORD: str | None = config["EMAIL_PASSWORD"]

if (EMAIL_USER is None) or (EMAIL_PASSWORD is None):
    logger.critical("EMAIL_USER or EMAIL_PASSWORD not found in .env file")
    sys.exit(1)

# Filter Criteria
FROM_ADDRESS: list[dict[str, str]] = [
    {"title": "Alpha Signal", "email": "alphasignal.ai"},  # news@alphasignal.ai
    {"title": "Byte Byte Go", "email": "bytebytego.com"},  # hi@digest.bytebytego.com
    {"title": "Google Gemini", "email": "google-gemini"},  # google-gemini-noreply@google.com
    {"title": "Ollama", "email": "ollama.com"},  # hello@ollama.com
    {"title": "Python Weekly", "email": "pythonweekly.com"},  # rahul@pythonweekly.com
    {"title": "Real Python", "email": "realpython.com"},  # info@realpython.com
    {"title": "Superhuman", "email": "superhuman"},  # superhuman@mail.joinsuperhuman.ai
    {"title": "The DeepView", "email": "thedeepview.co"},  # newsletter@thedeepview.co
    {"title": "The Rundown AI", "email": "therundown.ai"},  # news@daily.therundown.ai
    {"title": "Anthyme De Minutora", "email": "laminutora"},  # laminutora@10812296.brevosend.com
]

DAYS_AGO = 1  # Look back period

# --- DATABSE CONFIGURATION ---
DB_NAME: str = "IA_mails.db"

# --- IA CONFIGURATION ---
GOOGLE_API_KEY: str | None = config["GOOGLE_API_KEY"]
