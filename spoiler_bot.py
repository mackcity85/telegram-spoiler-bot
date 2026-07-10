import os
import threading

from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


TOKEN = os.getenv("BOT_TOKEN")


WARNING = """⚠️ Media Removed

This group requires all photos, videos, and GIFs to be sent using Telegram's Hide with Spoiler option.

Please resend your media with the spoiler enabled.
"""


app_web = Flask(__name__)


@app_web.route("/")
def home():
    return "Spoiler bot is running!"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(
        host="0.0.0.0",
        port=port
    )


async def check_media(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message

    if not message:
        return

    is_media = (
        message.photo
        or message.video
        or message.animation
    )

    if not is_media:
        return

    if message.has_media_spoiler:
        return

    try:
        await message.delete()

        await context.bot.send_message(
            chat_id=message.chat.id,
            text=WARNING
        )

        print("Removed non-spoiler media")

    except Exception as e:
        print("Error:", e)


def main():

    if not TOKEN:
        raise RuntimeError("BOT_TOKEN missing")

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()


    bot = Application.builder()\
        .token(TOKEN)\
        .build()


    bot.add_handler(
        MessageHandler(
            filters.ALL,
            check_media
        )
    )


    print("Spoiler moderation bot running")

    bot.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
