import os


# Telegram Bot Token
TOKEN = os.getenv(
    "BOT_TOKEN"
)


# Where startup messages are sent
# Add this in Render environment variables
STARTUP_CHAT_ID = os.getenv(
    "STARTUP_CHAT_ID"
)


# SQLite database
DB_FILE = "birthdays.db"


# Bot name
BOT_NAME = "Melanated AZ Community Bot"
