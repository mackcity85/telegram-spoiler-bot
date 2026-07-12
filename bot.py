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
    ContextTypes,
    filters
)

from config import BOT_TOKEN


# ==========================================================
# MODULE IMPORTS
# ==========================================================

from database import (
    initialize_database,
    update_member
)

from welcome import (
    welcome_new_member,
    profile_check,
    intro
)

from rules import rules

from admin import (
    admin_commands
)

from raffle import (
    start_raffle,
    enter_raffle,
    raffle_status,
    draw_raffle
)

from trivia import (
    trivia,
    trivia_answer
)

from truth_dare import (
    truth,
    dare
)

from birthday_scheduler import start_birthday_scheduler
from activity_scheduler import start_activity_scheduler
from pin_cleanup import pin_cleanup_task



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
            "Existing bot.lock found. Removing stale lock."
        )

        os.remove(LOCK_FILE)


    with open(LOCK_FILE,"w") as f:

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
# FLASK HEALTH CHECK
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
# MEDIA SPOILER PROTECTION
# ==========================================================


async def media_protection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message


    if not message:
        return



    # Allow GIFs

    if message.animation:

        return



    # Check photos

    bad_media = False


    if message.photo:

        if not message.has_media_spoiler:

            bad_media = True



    # Check videos

    if message.video:

        if not message.has_media_spoiler:

            bad_media = True



    if not bad_media:

        return



    try:

        await message.delete()


        warning = await update.effective_chat.send_message(

            "⚠️ Photos and videos must be sent with SPOILER enabled.\n\n"
            "Your message was removed."

        )


        await asyncio.sleep(
            30
        )


        await warning.delete()



    except Exception as e:

        logger.error(
            f"Media moderation error: {e}"
        )



# ==========================================================
# TRACK MEMBERS
# ==========================================================


async def track_activity(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user:

        update_member(

            update.effective_user.id,

            update.effective_chat.id,

            update.effective_user.username,

            update.effective_user.first_name

        )



# ==========================================================
# ERROR HANDLER
# ==========================================================


async def error_handler(
    update,
    context
):

    logger.error(
        "Bot error",
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


    logger.info(
        "Melanated AZ Bot started"
    )


    start_birthday_scheduler(
        application
    )


    start_activity_scheduler(
        application
    )


    asyncio.create_task(
        pin_cleanup_task(
            application
        )
    )



# ==========================================================
# MAIN
# ==========================================================


def main():


    initialize_database()



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
    # Welcome
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
    # Activity Tracking
    # --------------------------

    application.add_handler(

        MessageHandler(

            filters.ALL,

            track_activity

        ),

        group=5

    )



    # --------------------------
    # Media Protection
    # --------------------------

    application.add_handler(

        MessageHandler(

            filters.PHOTO |
            filters.VIDEO |
            filters.ANIMATION,

            media_protection

        ),

        group=1

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
    # Admin
    # --------------------------

    application.add_handler(

        CommandHandler(
            "admin",
            admin_commands
        )

    )



    # --------------------------
    # Raffle
    # --------------------------

    application.add_handler(

        CommandHandler(
            "startraffle",
            start_raffle
        )

    )


    application.add_handler(

        CommandHandler(
            "enter",
            enter_raffle
        )

    )


    application.add_handler(

        CommandHandler(
            "raffle",
            raffle_status
        )

    )


    application.add_handler(

        CommandHandler(
            "drawraffle",
            draw_raffle
        )

    )



    # --------------------------
    # Games
    # --------------------------

    application.add_handler(

        CommandHandler(
            "trivia",
            trivia
        )

    )


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            trivia_answer

        )

    )


    application.add_handler(

        CommandHandler(
            "truth",
            truth
        )

    )


    application.add_handler(

        CommandHandler(
            "dare",
            dare
        )

    )



    application.add_error_handler(
        error_handler
    )



    application.run_polling(
        drop_pending_updates=True
    )



# ==========================================================
# RUN
# ==========================================================


if __name__ == "__main__":

    main()
