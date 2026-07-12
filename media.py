# ==========================================================
# Melanated AZ Bot
# media.py
# Photo / Video Spoiler Protection
# GIFs Allowed
# ==========================================================

import asyncio

from telegram import Update
from telegram.ext import ContextTypes


WARNING_MESSAGE = """
🚫 Media Removed

Photos and videos must use Telegram Spoiler.

How to send with Spoiler:

1️⃣ Select your photo/video
2️⃣ Tap ⋮ menu
3️⃣ Choose "Hide with Spoiler"
4️⃣ Send again

✅ GIFs are allowed

Thank you for helping keep Melanated AZ organized.
"""


# ==========================================================
# DELETE WARNING AFTER 30 SECONDS
# ==========================================================

async def remove_warning(message):

    await asyncio.sleep(30)

    try:
        await message.delete()

    except Exception:
        pass



# ==========================================================
# MEDIA CHECK
# ==========================================================

async def check_media(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message


    if not message:
        return



    # Allow spoiler media

    if message.has_media_spoiler:
        return



    blocked = False



    # Photos

    if message.photo:

        blocked = True



    # Videos

    elif message.video:

        blocked = True



    # Videos sent as files

    elif message.document:

        mime = message.document.mime_type or ""

        if mime.startswith("video/"):

            blocked = True



    # GIFs/animations allowed



    if not blocked:

        return



    try:


        chat_id = message.chat.id



        # Delete bad media first

        await message.delete()



        # Send warning

        warning = await context.bot.send_message(

            chat_id=chat_id,

            text=WARNING_MESSAGE

        )


        # Remove warning after 30 seconds

        asyncio.create_task(

            remove_warning(
                warning
            )

        )


    except Exception as e:


        print(
            f"Media restriction error: {e}"
        )
