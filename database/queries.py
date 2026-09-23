CREATE_CATEGORIES_TABLE = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
"""

CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    photo_id TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
"""

INSERT_CATEGORY = """
INSERT OR IGNORE INTO categories (name)
VALUES (?)
"""

SELECT_CATEGORY_ID = """
SELECT id FROM categories
WHERE name = ?
"""

INSERT_PRODUCT = """
INSERT INTO products (name, price, category_id, photo_id)
VALUES (?, ?, ?, ?)
"""

SELECT_PRODUCTS_WITH_CATEGORIES = """
SELECT
    products.id,
    products.name,
    products.price,
    products.photo_id,
    categories.name AS category_name
FROM products
INNER JOIN categories
    ON products.category_id = categories.id
ORDER BY products.id DESC
"""

DELETE_PRODUCT = """
DELETE FROM products
WHERE id = ?
"""
