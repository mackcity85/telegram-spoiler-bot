# ==========================================================
# Melanated AZ Bot
# media.py
# Media Restriction System
# Photos/Videos Require Spoiler
# GIFs Allowed
# ==========================================================

import asyncio

from telegram import Update
from telegram.ext import ContextTypes


WARNING_MESSAGE = """
🚫 Media Removed

Photos and videos must be posted using Telegram Spoiler.

How to send:

1️⃣ Select your photo/video
2️⃣ Tap the ⋮ menu
3️⃣ Select "Hide with Spoiler"
4️⃣ Send again

GIFs are allowed ✅

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

async def media_protection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message


    if not message:

        return



    # ======================================================
    # ALLOW SPOILER MEDIA
    # ======================================================

    if getattr(
        message,
        "has_media_spoiler",
        False
    ):

        return



    blocked = False



    # ======================================================
    # BLOCK PHOTOS
    # ======================================================

    if message.photo:

        blocked = True



    # ======================================================
    # BLOCK VIDEOS
    # ======================================================

    elif message.video:

        blocked = True



    # ======================================================
    # BLOCK VIDEO DOCUMENTS
    # ======================================================

    elif message.document:

        mime_type = (
            message.document.mime_type
            or ""
        )


        if mime_type.startswith(
            "video/"
        ):

            blocked = True



    # ======================================================
    # ALLOW GIFS
    # ======================================================

    elif message.animation:

        return



    # ======================================================
    # REMOVE MEDIA
    # ======================================================

    if blocked:

        try:


            await message.delete()



            warning = await context.bot.send_message(

                chat_id=message.chat_id,

                text=WARNING_MESSAGE

            )


            asyncio.create_task(
                remove_warning(
                    warning
                )
            )


        except Exception as e:


            print(
                f"Media restriction error: {e}"
            )
