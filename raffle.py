# ==========================================================
# Melanated AZ Bot
# raffle.py
# ==========================================================


import random


from telegram import Update

from telegram.ext import ContextTypes


from database import (
    create_raffle,
    get_active_raffle,
    join_raffle,
    get_raffle_entries,
    close_raffle
)



# ==========================================================
# CREATE RAFFLE
# ==========================================================

async def create_raffle_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.args:

        await update.message.reply_text(
            "Usage:\n/createraffle Prize Name"
        )

        return


    title = " ".join(
        context.args
    )


    raffle_id = create_raffle(
        update.effective_chat.id,
        title
    )


    await update.message.reply_text(
        f"""
🎟️ NEW RAFFLE CREATED!

{title}

Enter now:

/joinraffle

Good luck 🔥
"""
    )



# ==========================================================
# VIEW RAFFLE
# ==========================================================

async def raffle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    raffle = get_active_raffle(
        update.effective_chat.id
    )


    if not raffle:

        await update.message.reply_text(
            "🎟️ No active raffle."
        )

        return



    await update.message.reply_text(
        f"""
🎟️ Current Raffle

{raffle[1]}

Join:

/joinraffle
"""
    )



# ==========================================================
# JOIN RAFFLE
# ==========================================================

async def join_raffle_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    raffle = get_active_raffle(
        update.effective_chat.id
    )


    if not raffle:

        await update.message.reply_text(
            "No active raffle."
        )

        return



    join_raffle(
        raffle[0],
        update.effective_user.id,
        update.effective_user.username,
        update.effective_user.first_name
    )


    await update.message.reply_text(
        "✅ You have been entered into the raffle!"
    )



# ==========================================================
# DRAW WINNER
# ==========================================================

async def draw_raffle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    raffle = get_active_raffle(
        update.effective_chat.id
    )


    if not raffle:

        await update.message.reply_text(
            "No active raffle."
        )

        return



    entries = get_raffle_entries(
        raffle[0]
    )


    if not entries:

        await update.message.reply_text(
            "No entries yet."
        )

        return



    winner = random.choice(
        entries
    )


    close_raffle(
        raffle[0]
    )


    await update.message.reply_text(
        f"""
🎉 RAFFLE WINNER 🎉

Congratulations {winner[2]}!

You won:

{raffle[1]}

🔥
"""
    )
