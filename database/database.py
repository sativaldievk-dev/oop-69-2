import sqlite3

from database.queries import (
    CREATE_CATEGORIES_TABLE,
    CREATE_PRODUCTS_TABLE,
    INSERT_CATEGORY,
    INSERT_PRODUCT,
    SELECT_CATEGORY_ID,
    SELECT_PRODUCTS_WITH_CATEGORIES,
)

DB_NAME = "bot.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(CREATE_CATEGORIES_TABLE)
    cursor.execute(CREATE_PRODUCTS_TABLE)

    conn.commit()
    conn.close()


def get_or_create_category(category_name: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(INSERT_CATEGORY, (category_name,))
    cursor.execute(SELECT_CATEGORY_ID, (category_name,))
    row = cursor.fetchone()

    conn.commit()
    conn.close()

    if row is None:
        raise RuntimeError("Не удалось получить ID категории")

    return row[0]


def add_product(name: str, price: int, category_id: int, photo_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        INSERT_PRODUCT,
        (name, price, category_id, photo_id)
    )

    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(SELECT_PRODUCTS_WITH_CATEGORIES)
    products = cursor.fetchall()

    conn.close()
    return products
