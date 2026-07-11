import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from birthdays import check_birthdays


scheduler = AsyncIOScheduler()


# ==========================
# START SCHEDULER
# ==========================

async def start_scheduler(app):

    if scheduler.running:
        return


    scheduler.add_job(
        check_birthdays,
        "cron",
        hour=9,
        minute=0,
        args=[app],
        id="birthday_check",
        replace_existing=True
    )


    scheduler.start()


    logging.info(
        "🎂 Birthday scheduler started"
    )
