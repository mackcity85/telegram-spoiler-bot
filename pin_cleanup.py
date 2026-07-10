import sqlite3
import logging

from datetime import datetime, timedelta

from config import DB_FILE



# ==========================
# RECORD PIN
# ==========================

async def record_pin(
    update,
    context
):

    message = update.effective_message


    if not message:

        return



    try:

        if message.pinned_message:


            pinned = message.pinned_message


            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()



            cursor.execute(

                """
                INSERT INTO pinned_messages
                (
                    chat_id,
                    message_id,
                    pinned_date
                )
                VALUES (?, ?, ?)
                """,

                (

                    update.effective_chat.id,

                    pinned.message_id,

                    datetime.now().isoformat()

                )

            )


            conn.commit()

            conn.close()



            logging.info(

                "Pinned message tracked"

            )


    except Exception as e:


        logging.exception(

            "Pin tracking failed: %s",

            e

        )



# ==========================
# REMOVE OLD PINS
# ==========================

async def cleanup_old_pins(
    app
):

    cutoff = datetime.now() - timedelta(

        days=90

    )


    conn = sqlite3.connect(

        DB_FILE

    )

    cursor = conn.cursor()



    cursor.execute(

        """
        SELECT chat_id, message_id
        FROM pinned_messages
        WHERE pinned_date < ?
        """,

        (

            cutoff.isoformat(),

        )

    )


    old_pins = cursor.fetchall()



    for chat_id, message_id in old_pins:


        try:

            await app.bot.unpin_chat_message(

                chat_id=chat_id,

                message_id=message_id

            )


            logging.info(

                "Unpinned old message %s",

                message_id

            )


            cursor.execute(

                """
                DELETE FROM pinned_messages
                WHERE chat_id=?
                AND message_id=?
                """,

                (

                    chat_id,

                    message_id

                )

            )


        except Exception as e:


            logging.warning(

                "Unable to unpin %s: %s",

                message_id,

                e

            )



    conn.commit()

    conn.close()
