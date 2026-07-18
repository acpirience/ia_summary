from dotenv import dotenv_values

# Load .env
config: dict[str, str | None] = dotenv_values(".env")


# --- EMAIL CONFIGURATION ---
IMAP_SERVER = "imap.gmail.com"

EMAIL_USER: str | None = config["EMAIL_USER"]
EMAIL_PASSWORD: str | None = config["EMAIL_PASSWORD"]

if (EMAIL_USER is None) or (EMAIL_PASSWORD is None):
    raise ValueError("EMAIL_USER or EMAIL_PASSWORD not found in .env file")

# Filter Criteria
FROM_ADDRESS: list[dict[str, str]] = [
    # AI
    {"title": "Alpha Signal", "email": "alphasignal.ai"},  # news@alphasignal.ai
    {"title": "Anthyme De Minutora", "email": "laminutora"},  # laminutora@10812296.brevosend.com
    {"title": "Byte Byte Go", "email": "bytebytego.com"},  # hi@digest.bytebytego.com
    {"title": "Superhuman", "email": "superhuman"},  # superhuman@mail.joinsuperhuman.ai
    {"title": "The DeepView", "email": "thedeepview.co"},  # newsletter@thedeepview.co
    {"title": "The Rundown AI", "email": "daily.therundown.ai"},  # news@daily.therundown.ai
    # tech
    {"title": "The Rundown Tech", "email": "technews.therundown.ai"},  # crew@technews.therundown.ai
    {"title": "TLDR", "email": "tldrnewsletter.com"},  # dan@tldrnewsletter.com
    {"title": "daily.dev", "email": "daily.dev"},  # informer@daily.dev
    {"title": "The Next Big Sh_t", "email": "the-nbs.fr"},  # luc@the-nbs.fr
    # python
    {"title": "PyCoder's Weekly", "email": "pycoders.com"},  # admin@pycoders.com
    {"title": "Python Weekly", "email": "pythonweekly.com"},  # rahul@pythonweekly.com
    {"title": "Real Python", "email": "realpython.com"},  # info@realpython.com
    # vendors
    {"title": "ChatGPT", "email": "email.openai.com"},  # noreply@email.openai.com
    {"title": "Claude", "email": "email.claude.com"},  # no-reply@email.claude.com
    {"title": "Google Gemini", "email": "google-gemini"},  # google-gemini-noreply@google.com
    {"title": "Napkin AI", "email": "contact@napkin.ai"},  # contact@napkin.ai
    {"title": "newline team", "email": "us@fullstack.io"},  # us@fullstack.io
    {"title": "Ollama", "email": "ollama.com"},  # hello@ollama.com
]

# --- STEP ---

STEPS: dict[int, str] = {
    0: "Pre-initialization",
    1: "cleanup HTML files",
    2: "Searching and reading emails",
    3: "Summarizing HTML files",
    4: "Deleting HTML files",
    5: "Git operations",
    6: "Stats",
}


DAYS_AGO = 2  # Look back period

# --- DATABSE CONFIGURATION ---
DB_NAME: str = "IA_mails.db"

# --- IA CONFIGURATION ---
GOOGLE_API_KEY: str | None = config["GOOGLE_API_KEY"]
