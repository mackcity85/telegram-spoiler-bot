import logging
import threading
import os

from flask import Flask

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import TOKEN, STARTUP_CHAT_ID

from database import init_db

from birthdays import (
    set_birthday,
    my_birthday,
    remove_birthday
)

from scheduler import start_scheduler

from raffles import (
    start_raffle,
    enter_raffle,
    raffle_list,
    draw_raffle
)


# ==========================
# LOGGING
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



# ==========================
# FLASK HEALTH CHECK
# ==========================

web_app = Flask(__name__)


@web_app.route("/")
def home():

    return "Melanated AZ Bot v2 is running!"



def run_web():

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    web_app.run(
        host="0.0.0.0",
        port=port
    )



# ==========================
# BASIC COMMANDS
# ==========================

async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🏓 Pong!\n\n"
        "Melanated AZ Bot v2 is online."
    )



async def get_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user
    chat = update.effective_chat


    await update.message.reply_text(

        f"👤 User ID: {user.id}\n"
        f"💬 Chat ID: {chat.id}"

    )



# ==========================
# STARTUP
# ==========================

async def startup(app):

    logging.info(
        "🤖 Melanated AZ Bot v2 started"
    )


    await start_scheduler(app)


    if STARTUP_CHAT_ID:

        try:

            await app.bot.send_message(

                chat_id=STARTUP_CHAT_ID,

                text=(

                    "🤖 Melanated AZ Bot v2 is online!\n\n"

                    "✅ Database Connected\n"
                    "✅ Birthday System Active\n"
                    "✅ Scheduler Running\n"
                    "✅ Raffle System Active\n\n"

                    "💜 Ready for the community!"

                )

            )

        except Exception as e:

            logging.error(
                "Startup message failed: %s",
                e
            )



# ==========================
# MAIN
# ==========================

def main():

    if not TOKEN:

        raise RuntimeError(
            "BOT_TOKEN missing"
        )



    # Initialize database

    init_db()



    # Start Render web server

    threading.Thread(

        target=run_web,

        daemon=True

    ).start()



    application = (

        Application
        .builder()
        .token(TOKEN)
        .post_init(startup)
        .build()

    )



    # ======================
    # COMMANDS
    # ======================


    application.add_handler(
        CommandHandler(
            "ping",
            ping
        )
    )


    application.add_handler(
        CommandHandler(
            "getid",
            get_id
        )
    )



    # ======================
    # BIRTHDAYS
    # ======================


    application.add_handler(
        CommandHandler(
            "birthday",
            set_birthday
        )
    )


    application.add_handler(
        CommandHandler(
            "mybirthday",
            my_birthday
        )
    )


    application.add_handler(
        CommandHandler(
            "removebirthday",
            remove_birthday
        )
    )



    # ======================
    # RAFFLES
    # ======================


    application.add_handler(
        CommandHandler(
            "raffle_start",
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
            "raffle_list",
            raffle_list
        )
    )


    application.add_handler(
        CommandHandler(
            "raffle_draw",
            draw_raffle
        )
    )



    logging.info(
        "🚀 Starting Telegram bot..."
    )



    application.run_polling(
        drop_pending_updates=True
    )



if __name__ == "__main__":

    main()
