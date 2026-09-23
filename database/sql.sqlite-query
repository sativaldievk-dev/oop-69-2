INSERT INTO products_detail (description, product_id, category)
VALUES ('Летние кроссы', 1000, 'обувь');


SELECT products.name,
       products.price,
       products_detail.description,
       products_detail.category,
       products.product_id,
       products_detail.product_id
FROM products
INNER JOIN products_detail
ON products.product_id = products_detail.product_id;


SELECT products.name,
       products.price,
       products_detail.description,
       products_detail.category,
       products.product_id,
       products_detail.product_id
FROM products
LEFT JOIN products_detail
ON products.product_id = products_detail.product_id;


SELECT products.name,
       products.price,
       products_detail.description,
       products_detail.category,
       products.product_id,
       products_detail.product_id
FROM products
RIGHT JOIN products_detail
ON products.product_id = products_detail.product_id;


SELECT products.name,
       products.price,
       products_detail.description,
       products_detail.category,
       products.product_id,
       products_detail.product_id
FROM products
FULL JOIN products_detail
ON products.product_id = products_detail.product_id;


UPDATE products
SET price = 5500
WHERE products.product_id = 1003;


SELECT *
FROM staff
WHERE user_id = 995712956;