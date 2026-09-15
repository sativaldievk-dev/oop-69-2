import sqlite3

DB_NAME = "database/database.db"


def add_user(name: str, age: int, gender: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, age, gender)
        VALUES (?, ?, ?)
        """,
        (name, age, gender)
    )

    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, age, gender FROM users")
    users = cursor.fetchall()

    conn.close()
    return users
