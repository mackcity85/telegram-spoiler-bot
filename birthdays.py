import sqlite3
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from config import DB_FILE


# ==========================
# DATABASE CHECK
# ==========================

def ensure_table():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS birthdays
        (
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            username TEXT,
            birthday TEXT,
            PRIMARY KEY(user_id, chat_id)
        )
        """
    )

    conn.commit()
    conn.close()



# ==========================
# SAVE BIRTHDAY
# ==========================

async def set_birthday(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    logging.info("🎂 /birthday command received")


    try:

        ensure_table()


        if not context.args:

            await update.message.reply_text(
                "🎂 Please use:\n\n"
                "/birthday MM/DD\n\n"
                "Example:\n"
                "/birthday 07/15"
            )

            return


        birthday = context.args[0]


        try:

            datetime.strptime(
                birthday,
                "%m/%d"
            )

        except ValueError:

            await update.message.reply_text(
                "❌ Invalid date.\n\n"
                "Use MM/DD format."
            )

            return



        user = update.effective_user
        chat = update.effective_chat


        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT OR REPLACE INTO birthdays
            (
                user_id,
                chat_id,
                username,
                birthday
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user.id,
                chat.id,
                user.first_name,
                birthday
            )
        )


        conn.commit()
        conn.close()



        logging.info(
            "🎂 Birthday saved for %s %s",
            user.first_name,
            birthday
        )


        await update.message.reply_text(
            "🎉 Birthday saved!\n\n"
            f"📅 {birthday}\n\n"
            "We will celebrate with you! 💜"
        )


    except Exception as e:

        logging.exception(
            "Birthday save failed"
        )


        await update.message.reply_text(
            f"❌ Birthday error:\n{e}"
        )



# ==========================
# VIEW BIRTHDAY
# ==========================

async def my_birthday(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    logging.info("🎂 /mybirthday command received")


    ensure_table()


    user = update.effective_user
    chat = update.effective_chat


    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT birthday
        FROM birthdays
        WHERE user_id=?
        AND chat_id=?
        """,
        (
            user.id,
            chat.id
        )
    )


    result = cursor.fetchone()

    conn.close()



    if result:

        await update.message.reply_text(
            "🎂 Your birthday:\n\n"
            f"📅 {result[0]}"
        )

    else:

        await update.message.reply_text(
            "❌ No birthday saved.\n\n"
            "Use:\n"
            "/birthday MM/DD"
        )



# ==========================
# REMOVE BIRTHDAY
# ==========================

async def remove_birthday(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    logging.info("🎂 /removebirthday command received")


    ensure_table()


    user = update.effective_user
    chat = update.effective_chat


    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM birthdays
        WHERE user_id=?
        AND chat_id=?
        """,
        (
            user.id,
            chat.id
        )
    )


    conn.commit()
    conn.close()



    await update.message.reply_text(
        "✅ Birthday removed."
    )



# ==========================
# DAILY BIRTHDAY CHECK
# ==========================

async def check_birthdays(app):

    ensure_table()


    today = datetime.now().strftime(
        "%m/%d"
    )


    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT username, chat_id
        FROM birthdays
        WHERE birthday=?
        """,
        (
            today,
        )
    )


    birthdays = cursor.fetchall()

    conn.close()



    for username, chat_id in birthdays:

        try:

            await app.bot.send_message(
                chat_id=chat_id,
                text=(
                    "🎉🎂 HAPPY BIRTHDAY! 🎂🎉\n\n"
                    f"Today we celebrate {username}! 💜"
                )
            )


        except Exception as e:

            logging.exception(
                "Birthday announcement failed: %s",
                e
            )
