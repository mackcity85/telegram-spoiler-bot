# ==========================================================
# Melanated AZ Bot
# birthdays.py
# Birthday System MM/DD
# ==========================================================

import logging
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from database import get_db


logger = logging.getLogger(__name__)


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def init_birthdays():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS birthdays
    (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        birthday TEXT
    )
    """)

    conn.commit()
    conn.close()



# ==========================================================
# /birthday MM/DD
# ==========================================================

async def birthday_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not user:
        return


    if not context.args:

        await update.message.reply_text(
            """
🎂 Birthday Setup

Use:

/birthday MM/DD

Example:

/birthday 07/25
"""
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
            """
❌ Invalid format.

Please use:

/birthday 07/25
"""
        )

        return



    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO birthdays
    (
        user_id,
        username,
        first_name,
        birthday
    )

    VALUES (?,?,?,?)

    ON CONFLICT(user_id)
    DO UPDATE SET

        username=excluded.username,
        first_name=excluded.first_name,
        birthday=excluded.birthday

    """,
    (
        user.id,
        user.username,
        user.first_name,
        birthday
    ))


    conn.commit()
    conn.close()



    await update.message.reply_text(
        f"""
🎂 Birthday Saved!

Your birthday: {birthday}

Thank you for sharing with Melanated AZ ❤️
"""
    )



# ==========================================================
# /birthdaycheck
# ==========================================================

async def birthday_check(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    today = datetime.now().strftime(
        "%m/%d"
    )


    conn = get_db()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT first_name, username
        FROM birthdays
        WHERE birthday = ?
        """,
        (today,)
    )


    birthdays = cursor.fetchall()

    conn.close()



    if not birthdays:

        await update.message.reply_text(
            "🎂 No birthdays today."
        )

        return



    message = "🎉 Today's Birthdays 🎉\n\n"


    for person in birthdays:

        name = (
            person[0]
            or person[1]
            or "Member"
        )

        message += f"🎂 {name}\n"


    await update.message.reply_text(
        message
    )
