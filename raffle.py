# ==========================================================
# Melanated AZ Bot
# raffle.py
# Raffle System
# ==========================================================

import random

from telegram import Update
from telegram.ext import ContextTypes

from admin import is_admin


raffle_data = {
    "active": False,
    "prize": "",
    "entries": []
}


# ==========================================================
# ADMIN CHECK HELPER
# ==========================================================

def check_admin(update):

    return is_admin(
        update.effective_user.id
    )


# ==========================================================
# START RAFFLE
# ==========================================================

async def start_raffle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not check_admin(update):

        await update.message.reply_text(
            "❌ Admins only."
        )
        return


    if not context.args:

        await update.message.reply_text(
            "Usage:\n/startraffle Prize Name"
        )
        return


    prize = " ".join(context.args)


    raffle_data["active"] = True
    raffle_data["prize"] = prize
    raffle_data["entries"] = []


    await update.message.reply_text(
        f"""
🎟️ RAFFLE STARTED 🎟️

🏆 Prize:
{prize}

Enter:
 /enter

Good luck!
"""
    )


# ==========================================================
# ENTER RAFFLE
# ==========================================================

async def enter_raffle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user


    if not raffle_data["active"]:

        await update.message.reply_text(
            "❌ No active raffle."
        )
        return


    if any(
        entry["id"] == user.id
        for entry in raffle_data["entries"]
    ):

        await update.message.reply_text(
            "✅ You are already entered."
        )
        return


    raffle_data["entries"].append(
        {
            "id": user.id,
            "name": user.first_name
        }
    )


    await update.message.reply_text(
        f"🎟️ {user.first_name}, you are entered!"
    )


# ==========================================================
# STATUS
# ==========================================================

async def raffle_status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not raffle_data["active"]:

        await update.message.reply_text(
            "No active raffle."
        )
        return


    await update.message.reply_text(
        f"""
🎟️ Current Raffle

🏆 Prize:
{raffle_data['prize']}

👥 Entries:
{len(raffle_data['entries'])}

Use:
/enter
"""
    )


# ==========================================================
# DRAW WINNER
# ==========================================================

async def draw_raffle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not check_admin(update):

        await update.message.reply_text(
            "❌ Admins only."
        )
        return


    if not raffle_data["entries"]:

        await update.message.reply_text(
            "❌ No entries."
        )
        return


    winner = random.choice(
        raffle_data["entries"]
    )


    prize = raffle_data["prize"]

    raffle_data["active"] = False


    await update.message.reply_text(
        f"""
🎉 RAFFLE WINNER 🎉

🏆 Prize:
{prize}

👑 Winner:
{winner['name']}

Congratulations!
"""
    )


# ==========================================================
# BOT IMPORT COMPATIBILITY
# ==========================================================

async def raffle_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await raffle_status(
        update,
        context
    )
