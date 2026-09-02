import sqlite3

# Подключение к базе данных
connection = sqlite3.connect("library.db")
cursor = connection.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
)
""")

connection.commit()


# CREATE — добавление книги
def create_book(title, author, price, quantity):
    cursor.execute("""
    INSERT INTO books (title, author, price, quantity)
    VALUES (?, ?, ?, ?)
    """, (title, author, price, quantity))

    connection.commit()
    print("Книга успешно добавлена!")


# READ — получение всех книг
def read_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if not books:
        print("В базе пока нет книг.")
        return

    print("\nСписок книг:")

    for book in books:
        print(
            f"ID: {book[0]} | "
            f"Название: {book[1]} | "
            f"Автор: {book[2]} | "
            f"Цена: {book[3]} | "
            f"Количество: {book[4]}"
        )


# UPDATE — изменение цены книги
def update_book(book_id, price):
    cursor.execute("""
    UPDATE books
    SET price = ?
    WHERE id = ?
    """, (price, book_id))

    connection.commit()

    if cursor.rowcount > 0:
        print("Цена книги обновлена!")
    else:
        print("Книга с таким ID не найдена.")


# DELETE — удаление книги
def delete_book(book_id):
    cursor.execute("""
    DELETE FROM books
    WHERE id = ?
    """, (book_id,))

    connection.commit()

    if cursor.rowcount > 0:
        print("Книга удалена!")
    else:
        print("Книга с таким ID не найдена.")


# Проверяем CRUD
create_book("1984", "George Orwell", 800, 5)
create_book("Мастер и Маргарита", "Михаил Булгаков", 900, 3)
create_book("Гарри Поттер", "J.K. Rowling", 1200, 7)

read_books()

update_book(1, 1000)

read_books()

delete_book(2)

read_books()


# Закрываем соединение
connection.close()