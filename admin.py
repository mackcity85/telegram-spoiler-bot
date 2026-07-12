from telegram import Update
from telegram.ext import ContextTypes

from database import get_member_count


# ==========================================================
# CHECK ADMIN
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

    for admin in admins:

        if admin.user.id == update.effective_user.id:
            return True


    return False



# ==========================================================
# ANNOUNCEMENT
# ==========================================================

async def announce(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await is_admin(update, context):

        await update.message.reply_text(
            "❌ Admins only."
        )

        return


    if not context.args:

        await update.message.reply_text(
            "Usage:\n/announce Your message here"
        )

        return


    message = " ".join(
        context.args
    )


    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "📢 MELANATED AZ ANNOUNCEMENT\n\n"
            f"{message}"
        )
    )



# ==========================================================
# BOT STATUS
# ==========================================================

async def botstatus(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await is_admin(update, context):

        await update.message.reply_text(
            "❌ Admins only."
        )

        return


    count = get_member_count()


    await update.message.reply_text(
        "✅ Melanated AZ Bot Status\n\n"
        "🟢 Online\n"
        "🛡 Media Protection Active\n"
        "🎂 Birthday System Active\n"
        "👋 Activity Tracking Active\n"
        f"👥 Members Tracked: {count}"
    )



# ==========================================================
# MEMBER COUNT
# ==========================================================

async def members(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await is_admin(update, context):

        await update.message.reply_text(
            "❌ Admins only."
        )

        return


    count = get_member_count()


    await update.message.reply_text(
        f"👥 Melanated AZ Members Tracked:\n\n{count}"
    )
