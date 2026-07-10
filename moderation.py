import logging

from telegram import Update
from telegram.ext import ContextTypes



WARNING = """
⚠️ Media Removed

This group requires all photos, videos, GIFs, and media files to be sent using Telegram's Hide with Spoiler option.

Please resend your media with the spoiler enabled.

How to do it:

1. Select your photo or video.
2. Tap the options menu.
3. Choose "Hide with Spoiler".
4. Send the media again.

Thank you for helping keep Melanated AZ comfortable for everyone. 💜
"""



async def is_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        member = await context.bot.get_chat_member(
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id
        )


        if member.status in [
            "administrator",
            "creator"
        ]:
            return True


    except Exception as e:

        logging.warning(
            "Admin check failed: %s",
            e
        )


    return False





async def check_media(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.effective_message


    if not message:

        return



    # Check media types

    is_media = False


    if message.photo:

        is_media = True


    elif message.video:

        is_media = True


    elif message.animation:

        is_media = True


    elif message.document:

        mime = message.document.mime_type


        if mime and (
            mime.startswith("image/")
            or mime.startswith("video/")
        ):

            is_media = True



    if not is_media:

        return



    # Admin bypass

    if await is_admin(
        update,
        context
    ):

        logging.info(
            "Admin media allowed"
        )

        return



    # Allow spoiler media

    if message.has_media_spoiler:

        logging.info(
            "Spoiler media allowed"
        )

        return



    # Remove bad media

    try:

        await message.delete()


        await context.bot.send_message(
            chat_id=message.chat.id,
            text=WARNING
        )


        logging.info(
            "Removed non-spoiler media from %s",
            message.from_user.username
            if message.from_user
            else "unknown"
        )


    except Exception as e:


        logging.exception(
            "Media removal failed: %s",
            e
        )
