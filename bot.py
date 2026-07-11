import threading

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN
from database import initialize_database, update_member
from moderation import check_media


app = Flask(__name__)


@app.route("/")
def home():
    return "🔥 Melanated AZ Community Bot v4 is running."


def run_flask():
    app.run(
        host="0.0.0.0",
        port=8080
    )


RULES_MESSAGE = """
🔥 Melanated AZ Community Guidelines 🔥

Welcome to the community!

📌 Please remember:

✅ Respect all members
✅ Consent and communication matter
✅ Protect everyone's privacy
✅ What is shared here stays here

⚠️ MEDIA SPOILER RULE

All photos, videos, GIFs, and media must use:

👁 Hide With Spoiler

How to use:

📱 Mobile:
1. Select your photo/video
2. Open media options
3. Choose "Hide With Spoiler"
4. Send

💻 Desktop:
1. Select your media
2. Right-click the preview
3. Choose "Hide With Spoiler"
4. Send

Thank you for helping keep Melanated AZ a safe space ❤️
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Melanated AZ Community Bot v4 is online!"
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"Chat ID:\n{update.effective_chat.id}"
    )


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        RULES_MESSAGE
    )


async def track_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user:
        update_member(update.effective_user)


def main():

    initialize_database()

    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )


    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    application.add_handler(
        CommandHandler(
            "getid",
            get_id
        )
    )


    application.add_handler(
        CommandHandler(
            "rules",
            rules
        )
    )


    application.add_handler(
        MessageHandler(
            filters.ALL,
            track_activity
        ),
        group=1
    )


    application.add_handler(
        MessageHandler(
            filters.ALL,
            check_media
        ),
        group=2
    )


    print(
        "🔥 Melanated AZ Community Bot v4 is running"
    )


    application.run_polling()


if __name__ == "__main__":

    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()

    main()
