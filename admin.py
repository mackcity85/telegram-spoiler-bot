# ==========================================================
# Melanated AZ Bot
# admin.py
# ==========================================================

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_IDS


# ==========================================================
# CHECK IF USER IS ADMIN
# ==========================================================

async def is_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not user:
        return False

    return user.id in ADMIN_IDS


# ==========================================================
# ADMIN HELP
# ==========================================================

async def admin_commands(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await is_admin(update, context):
        return

    await update.message.reply_text(
"""
👑 Admin Commands

🎟 Raffles
/startraffle <prize>
/drawraffle
/cancelraffle

📌 Group
/pin
/unpin

📜 Rules
/rules

🎂 Birthdays
/setbirthday MM-DD-YYYY

🎉 Activities
/activities

👥 Members
/inactive
/active

🛡 Moderation
/delete
"""
    )
