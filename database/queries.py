CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    category_id INTEGER NOT NULL
);
"""

CREATE_CATEGORIES_TABLE = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
"""

INSERT_CATEGORY = """
INSERT INTO categories (name)
VALUES (?);
"""

INSERT_PRODUCT = """
INSERT INTO products (name, price, category_id)
VALUES (?, ?, ?);
"""

SELECT_PRODUCTS_WITH_CATEGORIES = """
SELECT
    products.id,
    products.name,
    products.price,
    categories.name AS category
FROM products
INNER JOIN categories
    ON products.category_id = categories.id;
"""