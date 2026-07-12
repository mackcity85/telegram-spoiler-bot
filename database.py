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


    # Members

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



    # Pins

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pins
    (
        chat_id INTEGER,
        message_id INTEGER,
        description TEXT,
        pinned_date TEXT
    )
    """)



    conn.commit()
    conn.close()



# ==========================================================
# UPDATE MEMBER
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
# GET BIRTHDAYS
# ==========================================================

def get_birthdays_today(
    birthday
):

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
        chat_id,
        user_id,
        first_name

    FROM members

    WHERE birthday=?

    """,
    (
        birthday,
    ))


    results = cursor.fetchall()

    conn.close()

    return results



# ==========================================================
# MEMBER COUNT
# ==========================================================

def get_member_count():

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM members"
    )


    count = cursor.fetchone()[0]


    conn.close()

    return count



# ==========================================================
# ACTIVE MEMBERS
# ==========================================================

def get_active_members(
    cutoff
):

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
        user_id,
        chat_id,
        first_name

    FROM members

    WHERE last_active >= ?

    """,
    (
        cutoff,
    ))


    results = cursor.fetchall()

    conn.close()

    return results



# ==========================================================
# INACTIVE MEMBERS
# ==========================================================

def get_inactive_members(
    cutoff
):

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
        user_id,
        chat_id,
        first_name

    FROM members

    WHERE last_active < ?

    """,
    (
        cutoff,
    ))


    results = cursor.fetchall()

    conn.close()

    return results



# ==========================================================
# SAVE PIN
# ==========================================================

def save_pin(
    chat_id,
    message_id,
    description
):

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO pins
    (
        chat_id,
        message_id,
        description,
        pinned_date
    )

    VALUES (?, ?, ?, ?)

    """,
    (
        chat_id,
        message_id,
        description,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))


    conn.commit()
    conn.close()



# ==========================================================
# GET OLD PINS
# ==========================================================

def get_old_pins(
    cutoff
):

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
        chat_id,
        message_id

    FROM pins

    WHERE pinned_date < ?

    """,
    (
        cutoff.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    ))


    results = cursor.fetchall()

    conn.close()

    return results



# ==========================================================
# REMOVE PIN RECORD
# ==========================================================

def remove_pin(
    message_id
):

    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    DELETE FROM pins

    WHERE message_id=?

    """,
    (
        message_id,
    ))


    conn.commit()
    conn.close()

