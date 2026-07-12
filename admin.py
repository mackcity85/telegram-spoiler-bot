# ==========================================================
# Melanated AZ Bot
# admin.py
# Admin Protection System
# ==========================================================

from telegram import Update
from telegram.ext import ContextTypes


# ==========================================================
# CHECK ADMIN
# ==========================================================

async def is_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.effective_user:
        return False

    if not update.effective_chat:
        return False


    user_id = update.effective_user.id


    try:

        member = await context.bot.get_chat_member(
            update.effective_chat.id,
            user_id
        )


        return member.status in [
            "administrator",
            "creator"
        ]


    except Exception:

        return False



# ==========================================================
# ADMIN ONLY DECORATOR CHECK
# ==========================================================

async def require_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    allowed = await is_admin(
        update,
        context
    )


    if not allowed:

        await update.message.reply_text(
            "❌ This command is only available to admins."
        )

        return False


    return True



# ==========================================================
# ADMIN HELP
# ==========================================================

async def admin_help(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await require_admin(
        update,
        context
    ):
        return


    await update.message.reply_text(

        """
👑 Admin Commands

/remove - Remove a member
/ban - Ban a member
/unban - Unban a member
/warn - Warn a member

Future:
🎟 Raffle management
📢 Announcements
🧹 Cleanup tools
📊 Activity reports

"""
    )



# ==========================================================
# REMOVE MEMBER
# ==========================================================

async def remove_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await require_admin(
        update,
        context
    ):
        return


    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Reply to a user's message to remove them."
        )

        return


    user = update.message.reply_to_message.from_user


    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await context.bot.unban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await update.message.reply_text(
        f"👋 Removed {user.first_name} from the group."
    )



# ==========================================================
# BAN MEMBER
# ==========================================================

async def ban_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await require_admin(
        update,
        context
    ):
        return


    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Reply to a user's message to ban them."
        )

        return


    user = update.message.reply_to_message.from_user


    await context.bot.ban_chat_member(
        update.effective_chat.id,
        user.id
    )


    await update.message.reply_text(
        f"🚫 {user.first_name} has been banned."
    )
