# ==========================================================
# Melanated AZ Bot
# birthday_scheduler.py
# Automatic Birthday Announcements
# ==========================================================

import asyncio
import logging

from database import (
    get_todays_birthdays
)


logger = logging.getLogger(__name__)



# ==========================================================
# BIRTHDAY CHECK LOOP
# ==========================================================

async def birthday_check(
    application,
    chat_id
):


    logger.info(
        "Birthday scheduler started"
    )


    while True:

        try:

            birthdays = get_todays_birthdays()


            for birthday in birthdays:


                await application.bot.send_message(

                    chat_id=chat_id,

                    text=f"""
🎂🎉 HAPPY BIRTHDAY 🎉🎂

Everyone help us wish:

👑 {birthday['first_name']}

a very Happy Birthday!

Wishing you good vibes,
great experiences, and an amazing year ahead!

🎉 Melanated AZ Family
"""

                )



        except Exception as e:

            logger.error(

                f"Birthday scheduler error: {e}"

            )



        # Check every 24 hours

        await asyncio.sleep(
            86400
        )
