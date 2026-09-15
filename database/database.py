import aiosqlite
DB_NAME="products.db"

async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )""")
        await db.commit()

async def add_product(name, price):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO products (name,price) VALUES (?,?)",(name,price))
        await db.commit()

async def get_products():
    async with aiosqlite.connect(DB_NAME) as db:
        cur=await db.execute("SELECT name,price FROM products ORDER BY id")
        return await cur.fetchall()
