from abc import ABC, abstractmethod
import math


# ==========================================
# 1. ИНКАПСУЛЯЦИЯ
# ==========================================

class Person:
    def __init__(self):
        self._age = 0

    def set_age(self, age):
        if age < 0:
            print("Возраст не может быть отрицательным")
        else:
            self._age = age

    def get_age(self):
        return self._age


print("=== Инкапсуляция ===")

p = Person()
p.set_age(25)
print("Возраст:", p.get_age())

p.set_age(-5)


# ==========================================
# 2. НАСЛЕДОВАНИЕ
# ==========================================

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "I am an animal"


class Dog(Animal):
    def speak(self):
        return "Woof"


class Cat(Animal):
    def speak(self):
        return "Meow"


print("\n=== Наследование ===")

dog = Dog("Buddy")
cat = Cat("Kitty")

print(dog.name, dog.speak())
print(cat.name, cat.speak())


# ==========================================
# 3. ПОЛИМОРФИЗМ
# ==========================================

class Vehicle:
    def move(self):
        return "Vehicle is moving"


class Car(Vehicle):
    def move(self):
        return "Car is driving"


class Bicycle(Vehicle):
    def move(self):
        return "Bicycle is pedaling"


def move(vehicle):
    return vehicle.move()


print("\n=== Полиморфизм ===")

car = Car()
bike = Bicycle()

print(move(car))
print(move(bike))


# ==========================================
# 4. АБСТРАКЦИЯ
# ==========================================

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


print("\n=== Абстракция ===")

rect = Rectangle(10, 5)
circle = Circle(7)

print("Площадь прямоугольника:", rect.area())
print("Площадь круга:", round(circle.area(), 2))