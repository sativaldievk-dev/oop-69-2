import sqlite3

from database.queries import (
    CREATE_PRODUCTS_TABLE,
    CREATE_CATEGORIES_TABLE,
    INSERT_CATEGORY,
    SELECT_CATEGORY_ID,
    INSERT_PRODUCT,
    SELECT_PRODUCTS_WITH_CATEGORIES,
    DELETE_PRODUCT,
    DELETE_CATEGORY,
)

def create_tables():
    with sqlite3.connect("bot.db") as db:
        db.execute(CREATE_CATEGORIES_TABLE)
        db.execute(CREATE_PRODUCTS_TABLE)
        db.commit()


def add_category(name):
    with sqlite3.connect("bot.db") as db:
        db.execute(INSERT_CATEGORY, (name,))
        db.commit()


def get_category_id(name):
    with sqlite3.connect("bot.db") as db:
        cursor = db.execute(
            SELECT_CATEGORY_ID,
            (name,)
        )

        result = cursor.fetchone()

        if result:
            return result[0]

        return None


def add_product(name, price, category_id, photo_id=None):
    with sqlite3.connect("bot.db") as db:
        cursor = db.execute(
            INSERT_PRODUCT,
            (
                name,
                price,
                category_id,
                photo_id,
            )
        )

        db.commit()

        return cursor.lastrowid


def get_products_with_categories():
    with sqlite3.connect("bot.db") as db:
        cursor = db.execute(
            SELECT_PRODUCTS_WITH_CATEGORIES
        )

        return cursor.fetchall()

def delete_product(product_id):
    with sqlite3.connect("bot.db") as db:
        cursor = db.execute(
            "SELECT category_id FROM products WHERE id = ?",
            (product_id,)
        )

        result = cursor.fetchone()

        if result is None:
            return 0

        category_id = result[0]

        cursor = db.execute(
            DELETE_PRODUCT,
            (product_id,)
        )

        db.execute(
            DELETE_CATEGORY,
            (category_id,)
        )

        db.commit()

        return cursor.rowcount