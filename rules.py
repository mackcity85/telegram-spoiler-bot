# ==========================================================
# rules.py
# Melanated AZ Bot v3
# Community Rules
# ==========================================================

from telegram import Update
from telegram.ext import ContextTypes


RULES_TEXT = """

👑 Welcome to Melanated AZ 👑

Welcome everyone. This space was created for networking,
good vibes, and meeting like-minded people.

Please introduce yourself when joining and review the pinned
messages.

📸 Profile picture is required.

Include:

• Name
• Age
• Location
• Status (Single, Partnered, Poly, etc.)
• What you're here for
• DMs Open or Closed

Example:

King | 40 | Arizona | Partnered | Looking to network,
make connections, and meet like-minded people | DMs Open


━━━━━━━━━━━━━━━
📜 GROUP GUIDELINES
━━━━━━━━━━━━━━━


1️⃣ Consent Is Everything

• No means no.
• Respect boundaries at all times.
• No pressure, manipulation, or guilt trips.


2️⃣ Respect Everyone

• No bullying.
• No harassment.
• No discrimination.
• No personal attacks.

Different lifestyles, dynamics, and experience levels
are welcome.

Disagreements happen.
Disrespect does not.


3️⃣ Keep Drama Out

• Personal issues stay private.
• Do not bring outside conflicts into the group.
• Contact an admin if assistance is needed.


4️⃣ Privacy Matters

• What is shared here stays here.
• No screenshots or recordings without permission.
• Do not share personal information.


5️⃣ Adults Only

• Members must be 18+.
• No minors or discussion involving minors.


6️⃣ No Unsolicited Messages

• Ask before sending DMs.
• Respect someone's answer.
• Repeated unwanted contact may result in removal.


7️⃣ Verify Before You Trust

• Use good judgment.
• Prioritize your safety.
• The group is not responsible for individual interactions.


8️⃣ No Predatory Behavior

• Manipulation, coercion, intimidation,
  or abuse will not be tolerated.

Consent always comes first.


9️⃣ Keep It Classy

• Adult conversations are welcome.
• Avoid spam.
• Avoid excessive explicit content.
• Remember there are real people behind every profile.


🔟 Community First

• Support each other.
• Help newcomers.
• Leave egos at the door.


━━━━━━━━━━━━━━━
🔒 NSFW MEDIA & SPOILERS
━━━━━━━━━━━━━━━


To hide text:

1. Type your message.
2. Highlight the text.
3. Select "Spoiler".
4. Send the message.


To hide photos/videos:

1. Attach your photo or video.
2. Tap the three dots menu.
3. Select:

"Hide with Spoiler"

4. Send.


Media without proper spoiler protection may be removed.


━━━━━━━━━━━━━━━
👑 ADMIN RULE
━━━━━━━━━━━━━━━

Admins reserve the right to remove anyone whose behavior
negatively impacts the safety, privacy, or atmosphere
of the community.


Consent • Respect • Communication • Accountability

"""


async def rules(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        RULES_TEXT
    )
