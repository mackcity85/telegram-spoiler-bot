import sqlite3
from datetime import datetime


DB_NAME = "melanated_az.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_db():

    return sqlite3.connect(DB_NAME)



# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members
    (
        user_id INTEGER,
        chat_id INTEGER,
        username TEXT,
        first_name TEXT,
        joined_date TEXT,
        last_active TEXT,
        birthday TEXT,
        PRIMARY KEY(user_id, chat_id)
    )
    """)


    conn.commit()
    conn.close()



# ==========================================================
# UPDATE MEMBER ACTIVITY
# ==========================================================

def update_member(
        user_id,
        chat_id,
        username,
        first_name
):

    conn = get_db()
    cursor = conn.cursor()


    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute("""
    INSERT INTO members
    (
        user_id,
        chat_id,
        username,
        first_name,
        joined_date,
        last_active
    )
    VALUES (?, ?, ?, ?, ?, ?)

    ON CONFLICT(user_id, chat_id)

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
    ))


    conn.commit()
    conn.close()



# ==========================================================
# SAVE BIRTHDAY
# ==========================================================

def save_birthday(
        user_id,
        chat_id,
        birthday
):

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE members

    SET birthday=?

    WHERE user_id=?
    AND chat_id=?

    """,
    (
        birthday,
        user_id,
        chat_id
    ))


    conn.commit()
    conn.close()



# ==========================================================
# GET TODAY'S BIRTHDAYS
# ==========================================================

def get_birthdays_today(today):

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
        chat_id,
        user_id,
        first_name,
        username

    FROM members

    WHERE birthday=?

    """,
    (
        today,
    ))


    birthdays = cursor.fetchall()


    conn.close()


    return birthdays
