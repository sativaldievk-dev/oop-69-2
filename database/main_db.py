import sqlite3

from database.queries import (
    CREATE_PRODUCTS_TABLE,
    CREATE_CATEGORIES_TABLE,
    INSERT_CATEGORY,
    INSERT_PRODUCT,
    SELECT_PRODUCTS_WITH_CATEGORIES,
)


def create_tables():
    with sqlite3.connect("bot.db") as db:
        db.execute(CREATE_CATEGORIES_TABLE)
        db.execute(CREATE_PRODUCTS_TABLE)
        db.commit()


def add_category(name):
    with sqlite3.connect("bot.db") as db:
        cursor = db.execute(INSERT_CATEGORY, (name,))
        db.commit()
        return cursor.lastrowid


def add_product(name, price, category_id):
    with sqlite3.connect("bot.db") as db:
        db.execute(
            INSERT_PRODUCT,
            (name, price, category_id)
        )
        db.commit()


def get_products_with_categories():
    with sqlite3.connect("bot.db") as db:
        cursor = db.execute(SELECT_PRODUCTS_WITH_CATEGORIES)
        return cursor.fetchall()