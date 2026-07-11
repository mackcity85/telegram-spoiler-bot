import os
import sqlite3
import random
import logging
import threading

from datetime import datetime

from flask import Flask

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)



# ==========================
# CONFIG
# ==========================

TOKEN = os.getenv("BOT_TOKEN")
STARTUP_CHAT_ID = os.getenv("STARTUP_CHAT_ID")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


PAYMENT_INFO = """
💰 Raffle Entry Payment

Entry Fee: $5

Cash App: $YourName
Venmo: @YourName
PayPal: your@email.com

After payment type:

/joinraffle
"""


DB_FILE = "melanatedaz.db"



# ==========================
# LOGGING
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



# ==========================
# DATABASE
# ==========================

def init_db():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS birthdays (

            user_id INTEGER,
            chat_id INTEGER,
            username TEXT,
            birthday TEXT,

            PRIMARY KEY(
                user_id,
                chat_id
            )
        )
        """
    )


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS raffle_entries (

            user_id INTEGER PRIMARY KEY,
            username TEXT,
            date TEXT

        )
        """
    )


    conn.commit()

    conn.close()

    logging.info("✅ Database initialized")



# ==========================
# FLASK
# ==========================

web_app = Flask(__name__)


@web_app.route("/")
def home():

    return "Melanated AZ Bot is running!"



def run_web():

    port = int(
        os.getenv(
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

async def ping(update, context):

    await update.message.reply_text(
        "🏓 Pong!\n\nMelanated AZ Bot is online."
    )



async def get_id(update, context):

    await update.message.reply_text(

        f"👤 User ID: {update.effective_user.id}\n"
        f"💬 Chat ID: {update.effective_chat.id}"

    )



# ==========================
# BIRTHDAY SYSTEM
# ==========================

async def birthday(update, context):

    if not context.args:

        await update.message.reply_text(
            "Use:\n/birthday MM/DD\n\nExample:\n/birthday 07/15"
        )

        return


    date = context.args[0]

    user = update.effective_user
    chat = update.effective_chat


    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(

        """
        INSERT OR REPLACE INTO birthdays
        VALUES (?, ?, ?, ?)
        """,

        (
            user.id,
            chat.id,
            user.first_name,
            date
        )

    )


    conn.commit()
    conn.close()


    await update.message.reply_text(
        f"🎂 Birthday saved!\n\n📅 {date}"
    )



async def mybirthday(update, context):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(

        """
        SELECT birthday
        FROM birthdays
        WHERE user_id=?
        """,

        (
            update.effective_user.id,
        )

    )


    result = cursor.fetchone()

    conn.close()


    if result:

        await update.message.reply_text(
            f"🎂 Your birthday is {result[0]}"
        )

    else:

        await update.message.reply_text(
            "No birthday saved."
        )



async def removebirthday(update, context):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(

        """
        DELETE FROM birthdays
        WHERE user_id=?
        """,

        (
            update.effective_user.id,
        )

    )


    conn.commit()
    conn.close()


    await update.message.reply_text(
        "✅ Birthday removed."
    )



# ==========================
# RAFFLE SYSTEM
# ==========================

async def raffle(update, context):

    await update.message.reply_text(
        PAYMENT_INFO
    )



async def joinraffle(update, context):

    user = update.effective_user


    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(

        """
        INSERT OR IGNORE INTO raffle_entries
        VALUES (?, ?, ?)
        """,

        (
            user.id,
            user.first_name,
            datetime.now().strftime("%m/%d/%Y")
        )

    )


    conn.commit()

    conn.close()


    await update.message.reply_text(
        "🎟️ You have been entered into the raffle!"
    )



async def entries(update, context):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM raffle_entries"
    )


    count = cursor.fetchone()[0]


    conn.close()


    await update.message.reply_text(

        f"🎟️ Current Entries: {count}"

    )



async def drawraffle(update, context):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ Admin only."
        )

        return


    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(
        "SELECT username FROM raffle_entries"
    )


    users = [
        x[0]
        for x in cursor.fetchall()
    ]


    conn.close()


    if not users:

        await update.message.reply_text(
            "No entries yet."
        )

        return


    winner = random.choice(users)


    await update.message.reply_text(

        f"🎉 RAFFLE WINNER 🎉\n\n"
        f"🏆 {winner}\n\n"
        "Congratulations! 💜"

    )



# ==========================
# STARTUP
# ==========================

async def startup(app):

    logging.info(
        "🤖 Melanated AZ Bot Started"
    )


    if STARTUP_CHAT_ID:

        await app.bot.send_message(

            chat_id=STARTUP_CHAT_ID,

            text=(

                "💜 Melanated AZ Bot Online 💜\n\n"
                "✅ Birthday System\n"
                "✅ Raffle System\n"
                "✅ Payment Info\n"
                "✅ Database Connected"

            )

        )



# ==========================
# MAIN
# ==========================

def main():

    if not TOKEN:

        raise RuntimeError(
            "BOT_TOKEN missing"
        )


    init_db()


    threading.Thread(
        target=run_web,
        daemon=True
    ).start()


    app = (
        Application
        .builder()
        .token(TOKEN)
        .post_init(startup)
        .build()
    )


    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("getid", get_id))

    app.add_handler(CommandHandler("birthday", birthday))
    app.add_handler(CommandHandler("mybirthday", mybirthday))
    app.add_handler(CommandHandler("removebirthday", removebirthday))

    app.add_handler(CommandHandler("raffle", raffle))
    app.add_handler(CommandHandler("joinraffle", joinraffle))
    app.add_handler(CommandHandler("entries", entries))
    app.add_handler(CommandHandler("drawraffle", drawraffle))


    logging.info(
        "🚀 Starting Telegram bot..."
    )


    app.run_polling(
        drop_pending_updates=True
    )



if __name__ == "__main__":
    main()
