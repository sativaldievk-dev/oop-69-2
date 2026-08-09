from abc import ABC, abstractmethod


class Hero(ABC):

    def __init__(self, name, level, health, strength):
        self.name = name
        self.level = level
        self.health = health
        self.strength = strength

    def greet(self):
        print(f"Привет, я {self.name}, мой уровень {self.level}")

    def rest(self):
        print(f"{self.name} отдыхает")
        self.health += 1

    @abstractmethod
    def attack(self):
        pass


class Warrior(Hero):

    def attack(self):
        print("Воин атакует мечом")


class Mage(Hero):

    def attack(self):
        print("Маг использует магию")


class Assassin(Hero):

    def attack(self):
        print("Ассасин атакует из-под тишка")


# Создаём объекты
warrior = Warrior("Артур", 10, 100, 20)
mage = Mage("Мерлин", 12, 80, 15)
assassin = Assassin("Ниндзя", 11, 90, 25)


# Вызываем методы
warrior.greet()
warrior.attack()
warrior.rest()

print()

mage.greet()
mage.attack()
mage.rest()

print()

assassin.greet()
assassin.attack()
assassin.rest()