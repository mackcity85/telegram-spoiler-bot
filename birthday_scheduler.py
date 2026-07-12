# ==========================================================
# Melanated AZ Bot
# birthday_scheduler.py
# Birthday Announcement Scheduler
# ==========================================================

import asyncio
from datetime import datetime

from database import get_todays_birthdays



# ==========================================================
# BIRTHDAY CHECK
# ==========================================================

async def birthday_check(
    application
):

    while True:

        try:

            chat_id = application.bot_data.get(
                "STARTUP_CHAT_ID"
            )


            if not chat_id:

                await asyncio.sleep(86400)
                continue



            birthdays = get_todays_birthdays()



            for person in birthdays:


                name = person["first_name"]


                await application.bot.send_message(

                    chat_id=chat_id,

                    text=f"""
🎂🎉 HAPPY BIRTHDAY 🎉🎂

Everyone help us wish
👑 {name}

a very Happy Birthday!

May your day be filled with good energy,
great memories, and amazing moments.

🔥 Melanated AZ Family
"""
                )



        except Exception as e:

            print(
                "Birthday scheduler error:",
                e
            )



        # Check once every 24 hours

        await asyncio.sleep(
            60 * 60 * 24
        )
