import time
from functools import wraps


# =========================
# ЗАДАНИЕ 1 — ПРОВЕРКА АДМИНИСТРАТОРА
# =========================

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role


def is_admin(func):
    @wraps(func)
    def wrapper(user):
        if user.role == "admin":
            return func(user)
        else:
            print("У вас нет доступа")

    return wrapper


@is_admin
def delete_video(user):
    print("Видео удалено")


admin = User("Ardager", "admin")
user = User("Bek", "user")

delete_video(admin)
delete_video(user)


# =========================
# ЗАДАНИЕ 2 — ТАЙМЕР
# =========================

def timer(func):
    @wraps(func)
    def wrapper():
        start_time = time.time()

        result = func()

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Время выполнения: {execution_time:.1f} секунд")

        return result

    return wrapper


@timer
def download_video():
    time.sleep(2)
    print("Видео загружено")


download_video()