import asyncio
from datetime import datetime, timedelta

from database import (
    get_inactive_members,
    get_active_members
)


# ==========================================================
# 30 DAY MEMBER CHECK
# ==========================================================

async def activity_check(application):

    while True:

        cutoff = (
            datetime.now() - timedelta(days=30)
        ).strftime("%Y-%m-%d %H:%M:%S")


        # -----------------------------
        # Inactive Members
        # -----------------------------

        inactive = get_inactive_members(
            cutoff
        )


        for member in inactive:

            user_id = member[0]
            first_name = member[2]


            try:

                await application.bot.send_message(
                    chat_id=user_id,
                    text=(
                        f"👋 Hey {first_name}!\n\n"
                        "We haven't seen you around "
                        "Melanated AZ lately.\n\n"
                        "Just checking in — we hope "
                        "to see you back soon! ❤️"
                    )
                )


            except Exception:

                pass



        # -----------------------------
        # Active Members
        # -----------------------------

        active = get_active_members(
            cutoff
        )


        for member in active:

            user_id = member[0]
            first_name = member[2]


            try:

                await application.bot.send_message(
                    chat_id=user_id,
                    text=(
                        f"🔥 Thank you {first_name}!\n\n"
                        "We appreciate you being active "
                        "in the Melanated AZ community."
                    )
                )


            except Exception:

                pass



        # Run again every 30 days

        await asyncio.sleep(
            2592000
        )
