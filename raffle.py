# ==========================================================
# Melanated AZ Bot
# Raffle System
# ==========================================================

import random

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    create_raffle,
    add_raffle_entry,
    get_raffle_entries,
    clear_raffle
)


# ==========================================================
# SHOW RAFFLE
# ==========================================================

async def raffle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    await update.message.reply_text(
        "🎟 Melanated AZ Raffle 🎟\n\n"
        "Enter the current raffle by typing:\n\n"
        "/joinraffle\n\n"
        "Good luck! 👑"
    )


# ==========================================================
# JOIN RAFFLE
# ==========================================================

async def join_raffle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    user = update.effective_user


    add_raffle_entry(
        user.id,
        user.first_name,
        user.username
    )


    await update.message.reply_text(
        f"🎟 {user.first_name}, you are entered!\n\n"
        "Good luck in the raffle 👑"
    )



# ==========================================================
# CREATE RAFFLE
# ADMIN USE
# ==========================================================

async def start_raffle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    create_raffle()


    await update.message.reply_text(
        "🎟 New raffle started!\n\n"
        "Members can enter with:\n"
        "/joinraffle"
    )



# ==========================================================
# DRAW WINNER
# ADMIN USE
# ==========================================================

async def draw_winner(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    entries = get_raffle_entries()


    if not entries:

        await update.message.reply_text(
            "❌ No raffle entries found."
        )

        return



    winner = random.choice(
        entries
    )


    await update.message.reply_text(
        "🎉 RAFFLE WINNER 🎉\n\n"
        f"👑 {winner['first_name']}\n\n"
        "Congratulations!"
    )


    clear_raffle()
