import sqlite3

DB_NAME = "database/books.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books_detail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            genre TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    """)

    conn.commit()
    conn.close()