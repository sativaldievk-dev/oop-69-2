import aiosqlite


DB_PATH = "database/books.db"


async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL UNIQUE,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS books_detail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                genre TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        """)

        await db.commit()