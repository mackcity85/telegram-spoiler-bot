# ==========================================================
# Melanated AZ Bot
# activity_scheduler.py
# Member Activity Tracking & Reminders
# ==========================================================

import asyncio
import logging

from database import (
    get_inactive_members,
    get_active_members
)


logger = logging.getLogger(__name__)



# ==========================================================
# ACTIVITY CHECK LOOP
# ==========================================================

async def activity_check(
    application,
    chat_id
):


    logger.info(
        "Activity scheduler started"
    )


    while True:

        try:


            # Active member appreciation

            active_members = get_active_members(
                30
            )


            if active_members:

                names = ", ".join(

                    member["first_name"]

                    for member in active_members[:10]

                )


                await application.bot.send_message(

                    chat_id=chat_id,

                    text=f"""
👑 Community Appreciation 👑

Thank you to everyone staying active and contributing:

{names}

We appreciate the conversations,
connections, and positive energy!

🔥 Melanated AZ
"""

                )



            # Inactive member reminder list

            inactive_members = get_inactive_members(
                30
            )


            logger.info(

                f"Inactive members found: {len(inactive_members)}"

            )



        except Exception as e:


            logger.error(

                f"Activity scheduler error: {e}"

            )



        # Run every 30 days

        await asyncio.sleep(

            2592000

        )
