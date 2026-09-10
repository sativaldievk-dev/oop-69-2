-- Таблица пользователей
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Таблица книг
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Добавляем пользователей
INSERT INTO users (name)
VALUES ('ХАЯТИЛЛО');

INSERT INTO users (name)
VALUES ('Алекс');

-- Добавляем книги
INSERT INTO books (title, user_id)
VALUES ('Python для начинающих', 1);

INSERT INTO books (title, user_id)
VALUES ('SQL с нуля', 1);

INSERT INTO books (title, user_id)
VALUES ('HTML и CSS', 2);

-- Проверяем связь таблиц
SELECT users.name, books.title
FROM users
JOIN books ON users.id = books.user_id;