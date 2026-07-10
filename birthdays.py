import sqlite3
import logging

from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from config import DB_FILE



# ==========================
# SAVE BIRTHDAY
# ==========================

async def set_birthday(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.args:

        await update.message.reply_text(
            "🎂 Please use this format:\n\n"
            "/birthday MM/DD\n\n"
            "Example:\n"
            "/birthday 07/15"
        )

        return



    birthday = context.args[0]


    # Validate date

    try:

        datetime.strptime(
            birthday,
            "%m/%d"
        )


    except ValueError:

        await update.message.reply_text(
            "❌ Invalid date format.\n\n"
            "Please use MM/DD"
        )

        return



    user = update.effective_user
    chat = update.effective_chat



    conn = sqlite3.connect(
        DB_FILE
    )

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



    await update.message.reply_text(

        "🎉 Your birthday has been saved! 🎂\n\n"

        f"📅 Birthday: {birthday}\n\n"

        "Melanated AZ will celebrate with you "
        "on your special day! 🥳💜"

    )



# ==========================
# VIEW BIRTHDAY
# ==========================

async def my_birthday(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user
    chat = update.effective_chat



    conn = sqlite3.connect(
        DB_FILE
    )

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

            "🎂 Your saved birthday is:\n\n"
            f"📅 {result[0]}"

        )


    else:


        await update.message.reply_text(

            "You have not saved your birthday yet.\n\n"

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

    user = update.effective_user
    chat = update.effective_chat



    conn = sqlite3.connect(
        DB_FILE
    )

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

        "✅ Your birthday information has been removed."

    )



# ==========================
# DAILY CHECK
# ==========================

async def check_birthdays(
    app
):

    today = datetime.now().strftime(
        "%m/%d"
    )


    conn = sqlite3.connect(
        DB_FILE
    )

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

                    f"Today we celebrate {username}! 💜\n\n"

                    "Everyone help us show them some love "
                    "and make their day special! 🥳"

                )

            )


        except Exception as e:


            logging.exception(
                "Birthday announcement failed: %s",
                e
            )
