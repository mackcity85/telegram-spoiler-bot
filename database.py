# ==========================================================
# Melanated AZ Bot
# database.py
# ==========================================================

import sqlite3
from datetime import datetime


DATABASE = "melanatedaz.db"



# ==========================================================
# CONNECTION
# ==========================================================

def get_db():

    conn = sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn



# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    conn = get_db()

    cursor = conn.cursor()



    # Members

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS members
        (

            user_id INTEGER PRIMARY KEY,

            chat_id INTEGER,

            username TEXT,

            first_name TEXT,

            joined_date TEXT,

            last_active TEXT

        )
        """
    )



    # Birthdays

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS birthdays
        (

            user_id INTEGER PRIMARY KEY,

            chat_id INTEGER,

            birthday TEXT,

            username TEXT,

            first_name TEXT

        )
        """
    )



    # Raffles

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS raffle_entries
        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            chat_id INTEGER,

            user_id INTEGER,

            first_name TEXT,

            username TEXT,

            joined_at TEXT

        )
        """
    )



    conn.commit()

    conn.close()




# ==========================================================
# MEMBER UPDATE
# ==========================================================

def update_member(
    user_id,
    chat_id,
    username,
    first_name
):

    conn = get_db()

    cursor = conn.cursor()


    now = datetime.now().isoformat()



    cursor.execute(
        """
        INSERT INTO members
        (
            user_id,
            chat_id,
            username,
            first_name,
            joined_date,
            last_active
        )

        VALUES (?,?,?,?,?,?)

        ON CONFLICT(user_id)

        DO UPDATE SET

            username=?,
            first_name=?,
            last_active=?

        """,

        (

            user_id,
            chat_id,
            username,
            first_name,
            now,
            now,

            username,
            first_name,
            now

        )
    )



    conn.commit()

    conn.close()




# ==========================================================
# SAVE BIRTHDAY
# ==========================================================

def save_birthday(
    user_id,
    chat_id,
    birthday,
    username,
    first_name
):

    conn = get_db()

    cursor = conn.cursor()



    cursor.execute(
        """
        INSERT INTO birthdays
        (
            user_id,
            chat_id,
            birthday,
            username,
            first_name
        )

        VALUES (?,?,?,?,?)

        ON CONFLICT(user_id)

        DO UPDATE SET

            birthday=?,
            username=?,
            first_name=?

        """,

        (

            user_id,
            chat_id,
            birthday,
            username,
            first_name,

            birthday,
            username,
            first_name

        )
    )



    conn.commit()

    conn.close()




# ==========================================================
# GET TODAY BIRTHDAYS
# ==========================================================

def get_birthdays_today(
    birthday
):

    conn = get_db()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT *
        FROM birthdays
        WHERE birthday=?
        """,
        (
            birthday,
        )
    )


    results = cursor.fetchall()


    conn.close()


    return results




# ==========================================================
# RAFFLE ENTRY
# ==========================================================

def create_raffle_entry(
    chat_id,
    user_id,
    first_name,
    username
):

    conn = get_db()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT id
        FROM raffle_entries

        WHERE chat_id=?
        AND user_id=?

        """,

        (
            chat_id,
            user_id
        )
    )


    exists = cursor.fetchone()



    if not exists:


        cursor.execute(
            """
            INSERT INTO raffle_entries

            (
                chat_id,
                user_id,
                first_name,
                username,
                joined_at
            )

            VALUES (?,?,?,?,?)

            """,

            (

                chat_id,
                user_id,
                first_name,
                username,
                datetime.now().isoformat()

            )
        )



    conn.commit()

    conn.close()




# ==========================================================
# GET RAFFLE ENTRIES
# ==========================================================

def get_raffle_entries(
    chat_id
):

    conn = get_db()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT *
        FROM raffle_entries

        WHERE chat_id=?

        """,

        (
            chat_id,
        )
    )


    results = cursor.fetchall()



    conn.close()



    return results




# ==========================================================
# CLEAR RAFFLE
# ==========================================================

def clear_raffle_entries(
    chat_id
):

    conn = get_db()

    cursor = conn.cursor()



    cursor.execute(
        """
        DELETE FROM raffle_entries

        WHERE chat_id=?

        """,

        (
            chat_id,
        )
    )



    conn.commit()

    conn.close()
