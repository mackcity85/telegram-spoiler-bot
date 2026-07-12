# ==========================================================
# Melanated AZ Bot
# bot.py
# Main Bot Controller
# ==========================================================

import os
import asyncio
import logging
import threading


from flask import Flask


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
    update_activity
)


from welcome import (
    welcome_new_member,
    profile_check,
    intro
)


from rules import (
    rules
)


from activities import (
    activities,
    help_command
)


from birthdays import (
    set_birthday
)


from raffle import (
    start_raffle,
    enter_raffle,
    raffle_status,
    draw_raffle,
    cancel_raffle
)


from admin import (
    admin_commands
)


from trivia import (
    trivia,
    trivia_answer
)


from truth_dare import (
    truth,
    dare
)


from birthday_scheduler import (
    birthday_check
)


from activity_scheduler import (
    activity_check
)


from pin_cleanup import (
    pin_cleanup_task
)



# ==========================================================
# SETTINGS
# ==========================================================

STARTUP_CHAT_ID = int(
    os.environ.get(
        "STARTUP_CHAT_ID",
        "0"
    )
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
# ERROR HANDLER
# ==========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(

        "Bot error",

        exc_info=context.error

    )



# ==========================================================
# STARTUP TASKS
# ==========================================================

async def startup(
    application: Application
):


    await application.bot.delete_webhook(

        drop_pending_updates=True

    )


    print(
        "🔥 Melanated AZ Bot is running"
    )



    if STARTUP_CHAT_ID:


        asyncio.create_task(

            birthday_check(

                application,

                STARTUP_CHAT_ID

            )

        )


        asyncio.create_task(

            activity_check(

                application,

                STARTUP_CHAT_ID

            )

        )


        asyncio.create_task(

            pin_cleanup_task(

                application

            )

        )



# ==========================================================
# ACTIVITY TRACKER
# ==========================================================

async def track_activity(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):


    if update.effective_user:

        update_activity(

            update.effective_user.id

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



    # ======================================================
    # MEMBER SYSTEM
    # ======================================================


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



    # ======================================================
    # COMMANDS
    # ======================================================


    application.add_handler(

        CommandHandler(
            "rules",
            rules
        )

    )


    application.add_handler(

        CommandHandler(
            "help",
            help_command
        )

    )


    application.add_handler(

        CommandHandler(
            "activities",
            activities
        )

    )


    application.add_handler(

        CommandHandler(
            "setbirthday",
            set_birthday
        )

    )



    # ======================================================
    # RAFFLES
    # ======================================================


    application.add_handler(

        CommandHandler(
            "raffle",
            raffle_status
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
            "startraffle",
            start_raffle
        )

    )


    application.add_handler(

        CommandHandler(
            "drawraffle",
            draw_raffle
        )

    )


    application.add_handler(

        CommandHandler(
            "cancelraffle",
            cancel_raffle
        )

    )



    # ======================================================
    # GAMES
    # ======================================================


    application.add_handler(

        CommandHandler(
            "trivia",
            trivia
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



    # ======================================================
    # TEXT HANDLERS
    # ORDER MATTERS
    # ======================================================


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            trivia_answer

        )

    )


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            track_activity

        )

    )


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            profile_check

        )

    )



    # ======================================================
    # ADMIN
    # ======================================================


    application.add_handler(

        CommandHandler(
            "admin",
            admin_commands
        )

    )



    application.add_error_handler(

        error_handler

    )



    application.run_polling(

        drop_pending_updates=True

    )



# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    main()
