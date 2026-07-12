# ==========================================================
# Melanated AZ Bot
# welcome.py
# Member Welcome System
# ==========================================================

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    update_member
)



# ==========================================================
# NEW MEMBER WELCOME
# ==========================================================

async def welcome_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return



    for member in update.message.new_chat_members:


        # Ignore bot accounts

        if member.is_bot:
            continue



        update_member(

            member.id,
            update.effective_chat.id,
            member.username,
            member.first_name

        )



        await update.message.reply_text(

f"""
🔥 Welcome {member.first_name} to Melanated AZ! 👑

We are glad to have you here.

Before joining conversations, please:

📸 Add a profile picture

📝 Introduce yourself:

• Name
• Age
• Location
• Status
• What you're here for
• DMs Open or Closed


Example:

King | 40 | Arizona | Partnered | Networking & connections | DMs Open


Please review our community guidelines:

📜 /rules


Useful commands:

❓ /help
🎉 /activities
🎂 /setbirthday MM-DD-YYYY
🎟 /raffle


Respect • Consent • Communication • Good Energy

Welcome to the community! 👑
"""

        )



# ==========================================================
# PROFILE CHECK
# ==========================================================

async def profile_check(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    user = update.effective_user


    if not user:
        return



    try:

        photos = await context.bot.get_user_profile_photos(

            user.id,
            limit=1

        )


        if photos.total_count == 0:


            await update.message.reply_text(

                f"👋 {user.first_name}, "
                "please add a profile picture "
                "to complete your community profile."

            )


    except Exception:

        pass



# ==========================================================
# INTRO COMMAND
# ==========================================================

async def intro(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    if not context.args:


        await update.message.reply_text(

            "Usage:\n"
            "/intro Your introduction"

        )

        return



    introduction = " ".join(

        context.args

    )



    await update.message.reply_text(

f"""
✅ Introduction received!

{introduction}

Welcome to Melanated AZ 👑
"""

    )
