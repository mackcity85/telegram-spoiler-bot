import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from birthdays import check_birthdays



scheduler = None



# ==========================
# COMMUNITY TASK PLACEHOLDERS
# ==========================


async def run_feedback_poll():

    logging.info(
        "60-day community feedback poll check executed"
    )

    # Poll system will be added here



async def run_pin_cleanup():

    logging.info(
        "90-day pin cleanup check executed"
    )

    # Pin cleanup system will be added here



# ==========================
# START SCHEDULER
# ==========================


async def start_scheduler(app):

    global scheduler


    scheduler = AsyncIOScheduler()



    # Daily birthday check

    scheduler.add_job(

        check_birthdays,

        "cron",

        hour=9,

        minute=0,

        args=[app]

    )



    # Every 60 days

    scheduler.add_job(

        run_feedback_poll,

        "interval",

        days=60

    )



    # Daily pin cleanup check

    scheduler.add_job(

        run_pin_cleanup,

        "interval",

        days=1

    )



    scheduler.start()



    logging.info(

        "✅ Scheduler started"

    )
