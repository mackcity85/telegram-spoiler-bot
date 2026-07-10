import logging

from telegram import Update
from telegram.ext import ContextTypes



WELCOME_MESSAGE = """
💜 Welcome to Melanated AZ, {name}! 💜

We're glad you joined our community.

Please take a moment to introduce yourself:

• Name / Nickname
• Location
• What brought you here
• What you're looking forward to

Please review the group rules and help us keep this a welcoming space for everyone. 🙏

Welcome to the family! 🎉
"""



async def welcome_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:

        return



    for user in update.message.new_chat_members:


        try:

            await update.message.reply_text(

                WELCOME_MESSAGE.format(

                    name=user.first_name

                )

            )


            logging.info(

                "Welcomed new member %s",

                user.id

            )


        except Exception as e:


            logging.exception(

                "Welcome message failed: %s",

                e

            )
