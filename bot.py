# ==========================================================
# Melanated AZ Bot
# Main Bot Controller
# ==========================================================

import os
import sys
import atexit
import logging
import threading
import asyncio

from flask import Flask

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters
)


from config import BOT_TOKEN


# ==========================================================
# MODULE IMPORTS
# ==========================================================

from welcome import (
    welcome_new_member,
    profile_check,
    intro
)

from rules import (
    rules
)

from admin import (
    admin_commands
)

from raffle import (
    raffle_command
)

from database import (
    initialize_database,
    update_member
)


# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# ==========================================================
# SINGLE INSTANCE LOCK
# ==========================================================

LOCK_FILE = "bot.lock"


def acquire_lock():

    if os.path.exists(LOCK_FILE):

        print(
            "Another Melanated AZ Bot instance is running."
        )

        sys.exit(1)


    with open(LOCK_FILE, "w") as f:

        f.write(
            str(os.getpid())
        )


def release_lock():

    if os.path.exists(LOCK_FILE):

        os.remove(LOCK_FILE)


acquire_lock()

atexit.register(
    release_lock
)


# ==========================================================
# FLASK HEALTH CHECK FOR RENDER
# ==========================================================

app = Flask(__name__)


@app.route("/")
def home():

    return "Melanated AZ Bot Online"


def run_flask():

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )


# ==========================================================
# ERROR HANDLER
# ==========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Exception:",
        exc_info=context.error
    )


# ==========================================================
# STARTUP
# ==========================================================

async def startup(
    application: Application
):

    await application.bot.delete_webhook(
        drop_pending_updates=True
    )

    print(
        "Melanated AZ Bot is running"
    )


# ==========================================================
# MAIN
# ==========================================================

def main():


    initialize_database()


    # Start Render health server

    flask_thread = threading.Thread(
        target=run_flask,
        daemon=True
    )

    flask_thread.start()



    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(startup)
        .build()
    )


    # --------------------------
    # Welcome System
    # --------------------------

    application.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome_new_member
        )
    )


    application.add_handler(
        CommandHandler(
            "intro",
            intro
        )
    )


    application.add_handler(
        CommandHandler(
            "rules",
            rules
        )
    )


    # --------------------------
    # Profile Check
    # --------------------------

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            profile_check
        )
    )


    # --------------------------
    # Admin Commands
    # --------------------------

    admin_commands(
        application
    )


    # --------------------------
    # Raffle
    # --------------------------

    application.add_handler(
        CommandHandler(
            "raffle",
            raffle_command
        )
    )


    application.add_error_handler(
        error_handler
    )


    try:

        application.run_polling(
            drop_pending_updates=True
        )


    except KeyboardInterrupt:

        print(
            "Bot stopped"
        )


    finally:

        release_lock()



# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    main()
