import sqlite3

# A4 - пустая бумага
connect = sqlite3.connect('user.db')

# Рука и карандаш
cursor = connect.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        name VARCHAR(30) NOT NULL,
        age INTEGER NOT NULL,
        hobby TEXT
    )
''')

connect.commit()

# CRUD | Create-Read-Update-Delete

# Create
def create_user(name, age, hobby):
    cursor.execute(
        'INSERT INTO users(name, age, hobby) VALUES (?,?,?)',
        (name, age, hobby)
    )
    connect.commit()
    print(f'Пользователь {name} добавлен!')

# create_user('Петя', 13,'Игры, футбол, плавание')


# Read
def get_users():
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchmany(2)
    print(data)

get_users()

# Update
def update_user(name, rowid):
    cursor.execute(
        'UPDATE users SET name = ? WHERE rowid = ?',
        (name, rowid)
    )
    connect.commit()
    print("Пользователь обновлен!")

update_user('Петя', 3)

# Delete

def delete_user(rowid):
    cursor.execute(
        'DELETE FROM users WHERE rowid = ?',
        (rowid, )
    )
    connect.commit()
    print("Пользователь удален!")


delete_user(4)