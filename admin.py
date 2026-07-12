from telegram import Update
from telegram.ext import ContextTypes


# ==========================================================
# CHECK ADMIN
# ==========================================================

async def is_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id


    admins = await context.bot.get_chat_administrators(
        chat_id
    )


    for admin in admins:

        if admin.user.id == user_id:

            return True


    return False



# ==========================================================
# ANNOUNCEMENT COMMAND
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
            "Usage:\n/announce your message"
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


    await update.message.reply_text(
        "✅ Melanated AZ Bot Status\n\n"
        "🟢 Online\n"
        "🛡 Media Protection Active\n"
        "🎂 Birthday System Active\n"
        "👋 Activity Tracking Active"
    )
