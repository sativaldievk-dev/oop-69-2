import random


class Hero:
    def __init__(self, name, level, health, strength):
        self.name = name
        self.level = level
        self.health = health
        self.strength = strength

    def greet(self):
        print(f"Привет! Я {self.name}!")

    def attack(self):
        print(f"{self.name} атакует!")

    def rest(self):
        self.health += 10
        print(f"{self.name} отдыхает. Здоровье: {self.health}")


class Warrior(Hero):
    def __init__(self, name, level, health, strength, stamina):
        super().__init__(name, level, health, strength)
        self.stamina = stamina

    def attack(self):
        print("Воин атакует мечом!")


class Mage(Hero):
    def __init__(self, name, level, health, strength, mana):
        super().__init__(name, level, health, strength)
        self.mana = mana

    def attack(self):
        print("Маг кастует заклинание!")


class Assassin(Hero):
    def __init__(self, name, level, health, strength, stealth):
        super().__init__(name, level, health, strength)
        self.stealth = stealth

    def attack(self):
        print("Ассасин атакует из-под тишка!")


warrior = Warrior("Warrior", 10, 100, 20, 80)
mage = Mage("Mage", 10, 80, 25, 100)
assassin = Assassin("Assassin", 10, 90, 22, 95)

heroes = {
    "Warrior": warrior,
    "Mage": mage,
    "Assassin": assassin
}

print("Выберите героя:")
print("Warrior / Mage / Assassin")
choice = input(">>> ")

if choice not in heroes:
    print("Такого героя нет!")
else:
    player = heroes[choice]

    enemies = list(heroes.keys())
    enemies.remove(choice)
    enemy_name = random.choice(enemies)
    enemy = heroes[enemy_name]

    print(f"\nВы выбрали: {player.name}")
    print(f"Противник: {enemy.name}\n")

    player.attack()
    enemy.attack()

    if (
        (player.name == "Warrior" and enemy.name == "Assassin") or
        (player.name == "Assassin" and enemy.name == "Mage") or
        (player.name == "Mage" and enemy.name == "Warrior")
    ):
        print(f"\n{player.name} победил!")

    elif (
        (enemy.name == "Warrior" and player.name == "Assassin") or
        (enemy.name == "Assassin" and player.name == "Mage") or
        (enemy.name == "Mage" and player.name == "Warrior")
    ):
        print(f"\n{enemy.name} победил!")

    else:
        print("\nНичья!")