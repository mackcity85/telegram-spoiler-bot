import os
import threading

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("BOT_TOKEN")


WARNING = """⚠️ Media Removed

To help prevent accidental exposure, this group requires all pictures and videos to be sent using Telegram's Hide with Spoiler option.

Please resend your picture or video with the spoiler setting enabled.

How to do it:

1. Select your photo or video.
2. Before sending, tap the ⋮ menu (or options button).
3. Choose Hide with Spoiler.
4. Send the media again.

Thank you for helping keep the group comfortable and safe for everyone. 🙏
"""


# -------------------------
# Render Keep Alive
# -------------------------

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Spoiler bot is running!"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


# -------------------------
# Media Check
# -------------------------

async def check_media(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message

    if not message:
        return


    is_media = False


    # Normal photos
    if message.photo:
        is_media = True


    # Normal videos
    elif message.video:
        is_media = True


    # GIF / Animation
    elif message.animation:
        is_media = True


    # Images/videos sent as files
    elif message.document:

        mime = message.document.mime_type

        if mime:
            if (
                mime.startswith("image/")
                or mime.startswith("video/")
            ):
                is_media = True


    if not is_media:
        return


    # Allow Telegram spoiler media
    if message.has_media_spoiler:
        return


    try:
        await message.delete()

        await update.effective_chat.send_message(
            WARNING
        )

        print(
            f"Removed non-spoiler media from "
            f"{message.from_user.id}"
        )


    except Exception as e:
        print(
            "Media removal error:",
            e
        )


# -------------------------
# Main
# -------------------------

def main():

    if not TOKEN:
        raise ValueError(
            "BOT_TOKEN is missing"
        )


    # Start Render listener
    threading.Thread(
        target=run_web,
        daemon=True
    ).start()


    app = Application.builder().token(
        TOKEN
    ).build()


    media_filter = (
        filters.PHOTO
        | filters.VIDEO
        | filters.ANIMATION
        | filters.Document.ALL
    )


    app.add_handler(
        MessageHandler(
            media_filter,
            check_media
        )
    )


    print(
        "Spoiler moderation bot is running..."
    )


    app.run_polling()


if __name__ == "__main__":
    main()
