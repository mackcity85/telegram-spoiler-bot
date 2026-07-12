# ==========================================================
# Melanated AZ Bot
# activities.py
# Activities & Help Commands
# ==========================================================

from telegram import Update
from telegram.ext import ContextTypes



# ==========================================================
# /activities
# ==========================================================

async def activities(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    await update.message.reply_text(

"""
🎉 Melanated AZ Activities 👑

We host activities designed to help members connect:

🎲 Community Games

• Trivia
• Ice Breakers
• Polls
• Would You Rather
• Truth or Dare


🎟 Community Events

• Raffles
• Meet & Greets
• Group Kickbacks
• Networking Events


🎂 Member Recognition

• Birthday Shoutouts
• Member Appreciation


━━━━━━━━━━━━━━━

Useful Commands:

📜 /rules
View community guidelines

👋 /intro
Introduce yourself

🎂 /setbirthday MM-DD-YYYY
Save your birthday

🎟 /raffle
View current raffle

🎟 /enter
Enter raffle

❓ /help
View commands

━━━━━━━━━━━━━━━

More activities will be added regularly.

Have fun and enjoy the community! 👑
"""

    )



# ==========================================================
# /help
# ==========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    await update.message.reply_text(

"""
👑 Melanated AZ Bot Help

Community Commands

📜 /rules
View group guidelines

🎉 /activities
See community activities

👋 /intro
Post your introduction


🎂 Birthdays

/setbirthday MM-DD-YYYY


🎟 Raffles

/raffle
View current raffle

/enter
Join raffle


━━━━━━━━━━━━━━━

Admin Commands

/admin

(Admins only)

━━━━━━━━━━━━━━━

Enjoy the community! 👑
"""

    )
