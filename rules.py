# ==========================================================
# Melanated AZ Bot
# Rules and Guidelines
# ==========================================================

from telegram import Update
from telegram.ext import ContextTypes



RULES_TEXT = """
👑 Welcome to Melanated AZ 👑

Please introduce yourself when you join and review the pinned messages.

📸 A profile picture is required.

Include:

• Name
• Age
• Location
• Status (Single, Partnered, Poly, etc.)
• What you're here for
• DMs Open or Closed

Example:

King | 40 | Arizona | Partnered | 
Looking to network, make connections, and meet like-minded people |
DMs Open

━━━━━━━━━━━━━━━

📜 GROUP GUIDELINES 📜

1️⃣ Consent Is Everything

• No means no.
• Respect boundaries at all times.
• No pressure, manipulation, or guilt trips.

2️⃣ Respect Everyone

• No bullying.
• No harassment.
• No discrimination.
• No personal attacks.

Different lifestyles, dynamics, and experience levels are welcome.

3️⃣ Keep Drama Out

• Personal issues stay private.
• Do not bring outside conflicts into the group.
• Contact admins if help is needed.

4️⃣ Privacy Matters

• What is shared here stays here.
• No screenshots or recordings without permission.
• Do not share private information.

5️⃣ Adults Only

• All members must be 18+.
• No minors or inappropriate discussions involving minors.

6️⃣ No Unwanted Messages

• Ask before sending DMs.
• Respect "No".
• Repeated unwanted contact may result in removal.

7️⃣ Verify Before You Trust

• Protect your safety.
• Vet people before meeting.
• The group is not responsible for personal interactions.

8️⃣ No Predatory Behavior

• Manipulation, coercion, intimidation, or abuse will not be tolerated.

9️⃣ Keep It Classy

• Adult conversations are welcome.
• Avoid spam and excessive attention seeking.

🔟 Community First

• Support newcomers.
• Communicate respectfully.
• Leave egos at the door.

━━━━━━━━━━━━━━━

🔒 NSFW MEDIA & SPOILERS

To hide text:

1. Type your message.
2. Highlight the text.
3. Select "Spoiler".
4. Send.

To hide photos/videos:

1. Attach your photo or video.
2. Tap the three dots menu.
3. Select:

👁 Hide with Spoiler

4. Send your media.

All photos and videos must use Telegram spoiler protection.

━━━━━━━━━━━━━━━

🎉 GROUP ACTIVITIES

Use:

🎂 /birthday
Save your birthday.

🎲 /activities
See current activities.

🎟 /raffle
Enter upcoming raffles.

📜 /rules
View these guidelines.

━━━━━━━━━━━━━━━

👑 ADMIN RULE

Admins reserve the right to remove anyone who negatively impacts the safety, privacy, or atmosphere of the community.

Consent • Respect • Communication • Accountability
"""



# ==========================================================
# RULES COMMAND
# ==========================================================

async def rules(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    await update.message.reply_text(
        RULES_TEXT
    )
