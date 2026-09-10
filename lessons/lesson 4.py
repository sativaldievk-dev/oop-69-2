# Магические методы (их еще называют dunder-методами — от double underscore) —
# это специальные методы в Python, которые окружены двумя подчеркиваниями
# с каждой стороны: __название__.
# Их главная суть: они не вызываются вами напрямую. Они вызываются автоматически,
# когда вы используете определенные операторы или встроенные функции Python.

# | Оператор | Магический метод | Пример   |
# | -------- | ---------------- | -------- |
# | `+`      | `__add__`        | `a + b`  |
# | `-`      | `__sub__`        | `a - b`  |
# | `*`      | `__mul__`        | `a * b`  |
# | `/`      | `__truediv__`    | `a / b`  |
# | `//`     | `__floordiv__`   | `a // b` |
# | `%`      | `__mod__`        | `a % b`  |

# | Метод         | Что делает                |
# | ------------- | ------------------------- |
# | `__init__`    | конструктор               |
# | `__str__`     | вывод через `print()`     |
# | `__repr__`    | отображение объекта       |
# | `__len__`     | `len(obj)`                |
# | `__getitem__` | `obj[key]`                |
# | `__call__`    | вызов объекта как функции |
# | `__eq__`      | `==`                      |
# | `__lt__`      | `<`                       |
# | `__gt__`      | `>`                       |

class Test:
    def __init__(self, value):
        self.value = value

    # Это принт функция
    def __str__(self):
        return self.value

    def __add__(self, other):
        print(self.value)
        print(other.value)

    # def __getitem__(self, item):
    #     return self.value[item]


# test_obj = Test([1,2,3,4,5])
# test_obj_2 = Test(321)
# test_int = 123
# test_int_2 = 321
# amount_my_obj = test_obj + test_obj_2
# amount = test_int + test_int_2
# print(amount)
# print(amount_my_obj)
# my_list = [1,2,3,4]
# print(my_list[3])
# print(test_obj[4])


class Math:
    # Атрибута класса
    int_pi = 3.14

    def __init__(self, value_1, value_2):
        self.value_1 = value_1
        self.value_2 = value_2

    @staticmethod
    def add_sum(a, b):
        print(a + b)

    @classmethod
    def get_pi(cls):
        print(cls.int_pi)

    @property
    def get_sum(self):
        return self.value_1 + self.value_2

    @get_sum.setter
    def get_sum(self, value):
        self.value_1 = value

    def get_sum_2(self):
        return self.value_1 + self.value_2

obj_1 = Math(123, 321)
# Math.add_sum(12, 12)
# Math.get_pi()

# print(obj_1.value_1)
# obj_1.get_sum = 0000
# print(obj_1.value_1)

# публичный метод
# Защищеный
# Приватный
# Аблстрак метод
# Магические методы
# Статик метод
# класс метод
# Проперти метод

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency


    def __add__(self, other):
        if self.currency == other.currency:
            print(self.amount + other.amount)
        else:
            print("разные валюты")


# usd = Money(100, 'som')
# som = Money(100, 'som')
# total_sum_wallet = usd + som


class Client:

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.view_count = 0

    def __call__(self, *args, **kwargs):
        self.view_count +=1

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

client_1 = Client('John', 'Doe')
client_2 = Client(client_1, 'Doe')
client_3 = Client('John', 'Doe')
client_4 = Client('John', 'Doe')
print(client_1.view_count)
client_1()
print(client_1.view_count)

import random
# *
__all__ = (
    'Money',
    'Math',
    'random'
)


import requests


data = requests.get('http://localhost:8001/api/v1/customers/4436937/cashbacks/history?offset=0&limit=50')
print(data.request)