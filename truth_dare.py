import random

from telegram import Update
from telegram.ext import ContextTypes



# ==========================================================
# TRUTH QUESTIONS
# ==========================================================

TRUTHS = {

    "safe": [

        "What is one thing people would be surprised to know about you?",
        "What is your favorite way to spend a weekend?",
        "What is a goal you are working toward?"

    ],


    "spicy": [

        "What is your biggest turn-on?",
        "What is something you find attractive in a person?",
        "What is your favorite date idea?"

    ],


    "edge": [

        "What is a fantasy you have never shared?",
        "What is something adventurous you want to try?",
        "What is your biggest temptation?"

    ],


    "chaos": [

        "What is the boldest thing you have ever done?",
        "What is something you have always wanted to admit?",
        "What is your wildest story?"

    ]

}



# ==========================================================
# DARE QUESTIONS
# ==========================================================

DARES = {

    "safe": [

        "Send a positive compliment to someone.",
        "Share your favorite song.",
        "Tell the group something funny about yourself."

    ],


    "spicy": [

        "Describe your perfect date.",
        "Share your biggest attraction.",
        "Give someone a genuine compliment."

    ],


    "edge": [

        "Share a secret fantasy (if comfortable).",
        "Describe your ideal adventure.",
        "Tell a story you normally keep private."

    ],


    "chaos": [

        "Tell your most unexpected story.",
        "Share your most adventurous experience.",
        "Answer the next question honestly."

    ]

}



# ==========================================================
# TRUTH COMMAND
# ==========================================================

async def truth(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    level = "safe"


    if context.args:

        level = context.args[0].lower()


    if level not in TRUTHS:

        level = "safe"


    question = random.choice(
        TRUTHS[level]
    )


    await update.message.reply_text(
        f"🔥 TRUTH ({level.upper()})\n\n"
        f"{question}"
    )



# ==========================================================
# DARE COMMAND
# ==========================================================

async def dare(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    level = "safe"


    if context.args:

        level = context.args[0].lower()


    if level not in DARES:

        level = "safe"


    challenge = random.choice(
        DARES[level]
    )


    await update.message.reply_text(
        f"🔥 DARE ({level.upper()})\n\n"
        f"{challenge}"
    )
