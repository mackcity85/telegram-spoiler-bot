import asyncio
import logging

from datetime import datetime, timedelta

from database import (
    get_active_members,
    get_inactive_members
)


logging.basicConfig(level=logging.INFO)



async def activity_check(application):

    logging.info(
        "Activity scheduler started"
    )


    try:

        while True:


            cutoff = (
                datetime.now()
                -
                timedelta(days=30)
            )


            active = get_active_members(
                cutoff
            )


            inactive = get_inactive_members(
                cutoff
            )


            logging.info(
                f"Active members: {len(active)}"
            )


            logging.info(
                f"Inactive members: {len(inactive)}"
            )



            await asyncio.sleep(
                2592000
            )



    except asyncio.CancelledError:

        logging.info(
            "Activity scheduler stopped cleanly"
        )

        raise
