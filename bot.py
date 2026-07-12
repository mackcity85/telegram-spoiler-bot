# ==========================================================
# Melanated AZ Bot
# Main Launcher
# ==========================================================

import os
import logging
from threading import Thread

from dotenv import load_dotenv
from flask import Flask

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    filters
)


# ==========================================================
# ENV
# ==========================================================

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

STARTUP_CHAT_ID = os.getenv(
    "STARTUP_CHAT_ID"
)


if not TOKEN:
    raise ValueError(
        "BOT_TOKEN missing"
    )


# ==========================================================
# IMPORTS
# ==========================================================

from admin import admin_commands

from media import check_media

from welcome import welcome

from birthdays import (
    init_birthdays,
    birthday_command,
    birthday_check
)

from rules import rules

from raffle import (
    startraffle,
    drawraffle,
    cancelraffle
)

from trivia import trivia

from truth_dare import truth_or_dare



# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)



# ==========================================================
# KEEP ALIVE
# ==========================================================

app = Flask(__name__)


@app.route("/")
def home():

    return "Melanated AZ Bot Running"



def run_web():

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                10000
            )
        )
    )



# ==========================================================
# STARTUP MESSAGE
# ==========================================================

async def startup_message(application):

    if STARTUP_CHAT_ID:

        try:

            await application.bot.send_message(
                chat_id=int(STARTUP_CHAT_ID),
                text=
                "🟢 Melanated AZ Bot is online\n\n"
                "🛡 Media Protection Active\n"
                "🎂 Birthday System Active"
            )

        except Exception as e:

            logger.warning(
                f"Startup message failed: {e}"
            )



# ==========================================================
# MAIN
# ==========================================================

def main():


    Thread(
        target=run_web,
        daemon=True
    ).start()



    init_birthdays()



    bot = (
        Application
        .builder()
        .token(TOKEN)
        .post_init(startup_message)
        .build()
    )



    # =========================
    # COMMANDS
    # =========================


    bot.add_handler(
        CommandHandler(
            "admin",
            admin_commands
        )
    )


    bot.add_handler(
        CommandHandler(
            "birthday",
            birthday_command
        )
    )


    bot.add_handler(
        CommandHandler(
            "birthdaycheck",
            birthday_check
        )
    )


    bot.add_handler(
        CommandHandler(
            "rules",
            rules
        )
    )


    bot.add_handler(
        CommandHandler(
            "trivia",
            trivia
        )
    )


    bot.add_handler(
        CommandHandler(
            "truth",
            truth_or_dare
        )
    )


    bot.add_handler(
        CommandHandler(
            "startraffle",
            startraffle
        )
    )


    bot.add_handler(
        CommandHandler(
            "drawraffle",
            drawraffle
        )
    )


    bot.add_handler(
        CommandHandler(
            "cancelraffle",
            cancelraffle
        )
    )



    # =========================
    # MEDIA PROTECTION
    # ONLY PHOTOS/VIDEOS
    # =========================


    bot.add_handler(
        MessageHandler(
            (
                filters.PHOTO
                |
                filters.VIDEO
                |
                filters.Document.VIDEO
            ),
            check_media
        ),
        group=1
    )



    # =========================
    # WELCOME
    # =========================

    bot.add_handler(
        ChatMemberHandler(
            welcome,
            ChatMemberHandler.CHAT_MEMBER
        )
    )



    print(
        "🟢 Melanated AZ Bot Started"
    )



    bot.run_polling(
        allowed_updates=None,
        drop_pending_updates=True
    )



if __name__ == "__main__":

    main()
