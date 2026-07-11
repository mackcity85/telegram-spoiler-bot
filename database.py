import sqlite3
import os

from config import DB_FILE


def init_db():

    os.makedirs(
        "data",
        exist_ok=True
    )


    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS members
        (
            user_id INTEGER,
            chat_id INTEGER,
            username TEXT,
            first_seen TEXT,
            last_seen TEXT,
            PRIMARY KEY(user_id, chat_id)
        )
        """
    )


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS birthdays
        (
            user_id INTEGER,
            chat_id INTEGER,
            username TEXT,
            birthday TEXT,
            PRIMARY KEY(user_id, chat_id)
        )
        """
    )


    conn.commit()

    conn.close()
