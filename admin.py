# ==========================================================
# Melanated AZ Bot
# admin.py
# Admin Protection & Commands
# ==========================================================

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_IDS



# ==========================================================
# CHECK ADMIN
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
# ADMIN COMMAND MENU
# ==========================================================

async def admin_commands(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    if not await is_admin(
        update,
        context
    ):

        await update.message.reply_text(
            "❌ Admins only."
        )

        return



    await update.message.reply_text(

"""
👑 Melanated AZ Admin Commands

🎟 Raffles

/startraffle Prize Name
Start a raffle

/drawraffle
Pick winner

/cancelraffle
Cancel raffle


👥 Members

/active
Show active members

/inactive
Show inactive members


🎂 Birthdays

/birthdaycheck
Check today's birthdays


📌 Group Tools

/pin
Pin messages

/unpin
Remove pins


🛡 Moderation

/delete
Delete message


━━━━━━━━━━━━━━━

Admin access confirmed 👑
"""
    )
