# ==========================================================
# Melanated AZ Bot
# media.py
# Media Restriction System
# Photos/Videos Require Spoiler
# GIFs Allowed
# Deletes warning after 30 seconds
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

async def check_media(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message


    if not message:
        return



    # Ignore admins
    # (optional - remove if you want admins restricted too)

    if update.effective_user.id in [5879167814]:

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



    # Video files uploaded as documents

    elif message.document:

        mime = message.document.mime_type or ""

        if mime.startswith("video/"):

            blocked = True



    # GIF
