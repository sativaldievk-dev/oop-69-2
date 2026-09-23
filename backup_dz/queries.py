# database/queries.py

# Запросы для удаления товара.
# Товар хранится в двух связанных таблицах.
# Удаляем по общему полю product_id.

DELETE_PRODUCT = """
DELETE FROM products
WHERE product_id = ?;
"""

DELETE_PRODUCT_INFO = """
DELETE FROM product_info
WHERE product_id = ?;
"""
