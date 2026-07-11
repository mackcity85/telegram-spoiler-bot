import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

STARTUP_CHAT_ID = int(os.getenv("STARTUP_CHAT_ID", "0"))

ADMIN_IDS = [
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip()
]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing from .env")
