import sqlite3
import logging

from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from config import DB_FILE



# ==========================
# MEMBER SUGGESTIONS
# ==========================

async def suggestion(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    if not context.args:


        await update.message.reply_text(

            "💡 Please enter your suggestion.\n\n"

            "Example:\n"
            "/suggestion Add more community events"

        )

        return



    text = " ".join(

        context.args

    )


    user = update.effective_user



    conn = sqlite3.connect(

        DB_FILE

    )

    cursor = conn.cursor()



    cursor.execute(

        """
        INSERT INTO suggestions
        (
            user_id,
            username,
            suggestion,
            created
        )
        VALUES (?, ?, ?, ?)
        """,

        (

            user.id,

            user.first_name,

            text,

            datetime.now().isoformat()

        )

    )


    conn.commit()

    conn.close()



    await update.message.reply_text(

        "💜 Thank you for your suggestion!\n\n"

        "Your feedback has been saved and will "
        "be reviewed during community check-ins."

    )



# ==========================
# AUTOMATIC POLL PLACEHOLDER
# ==========================

async def create_feedback_poll(
    app
):


    logging.info(

        "Creating 60-day feedback poll"

    )


    # Future poll questions will go here


    return
