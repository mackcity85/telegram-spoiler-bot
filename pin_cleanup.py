import asyncio
from datetime import datetime, timedelta


# ==========================================================
# PIN CLEANUP SYSTEM
# ==========================================================

async def pin_cleanup(application):

    while True:

        await asyncio.sleep(
            86400
        )


        # This will run daily
        # Telegram does not provide pin age directly,
        # so we will track bot pins in the database
        # in the next database update.

        print(
            f"Pin cleanup check: {datetime.now()}"
        )
