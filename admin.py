# ==========================================================
# admin.py
# Melanated AZ Bot v3
# Admin Protection + Moderation Commands
# ==========================================================

import logging

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)


# ==========================================================
# ADMIN CHECK
# ==========================================================

async def is_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.effective_user:
        return False

    admins = await context.bot.get_chat_administrators(
        update.effective_chat.id
    )

    return any(
        admin.user.id == update.effective_user.id
        for admin in admins
    )



async def admin_only(
    update,
    context
):

    if not await is_admin(update, context):

        await update.message.reply_text(
            "❌ Admins only."
        )

        return False

    return True



# ==========================================================
# ANNOUNCE
# ==========================================================

async def announce(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await admin_only(update, context):
        return


    if not context.args:

        await update.message.reply_text(
            "Usage:\n"
            "/announce message"
        )

        return


    message = " ".join(
        context.args
    )


    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"📢 Announcement\n\n{message}"
    )



# ==========================================================
# PURGE
# ==========================================================

async def purge(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await admin_only(update, context):
        return


    if not context.args:

        await update.message.reply_text(
            "Usage:\n"
            "/purge number"
        )

        return


    amount = int(
        context.args[0]
    )


    message_id = update.message.id


    for i in range(amount):

        try:

            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=message_id-i
            )

        except:

            pass



# ==========================================================
# KICK
# ==========================================================

async def kick(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await admin_only(update, context):
        return


    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Reply to a user to kick."
        )

        return


    user = (
        update.message
        .reply_to_message
        .from_user
    )


    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await context.bot.unban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await update.message.reply_text(
        f"👢 Removed {user.first_name}"
    )



# ==========================================================
# BAN
# ==========================================================

async def ban(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await admin_only(update, context):
        return


    if not update.message.reply_to_message:
        return


    user = (
        update.message
        .reply_to_message
        .from_user
    )


    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await update.message.reply_text(
        f"🚫 Banned {user.first_name}"
    )



# ==========================================================
# MUTE
# ==========================================================

async def mute(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await admin_only(update, context):
        return


    if not update.message.reply_to_message:
        return


    user = (
        update.message
        .reply_to_message
        .from_user
    )


    permissions = ChatPermissions(
        can_send_messages=False
    )


    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions
    )


    await update.message.reply_text(
        f"🔇 Muted {user.first_name}"
    )



# ==========================================================
# UNMUTE
# ==========================================================

async def unmute(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await admin_only(update, context):
        return


    if not update.message.reply_to_message:
        return


    user = (
        update.message
        .reply_to_message
        .from_user
    )


    permissions = ChatPermissions(
        can_send_messages=True
    )


    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions
    )


    await update.message.reply_text(
        f"🔊 Unmuted {user.first_name}"
    )
