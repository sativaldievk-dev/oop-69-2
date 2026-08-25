# ==========================================
# 1. БАЗОВЫЙ КЛАСС HERO
# ==========================================

class Hero:
    def __init__(self, name, lvl, hp):
        self.name = name
        self.lvl = lvl
        self.hp = hp

    def action(self):
        print(f"{self.name} готов к бою!")


# ==========================================
# 2. ДОЧЕРНИЕ КЛАССЫ
# ==========================================

class MageHero(Hero):
    def __init__(self, name, lvl, hp, mp):
        super().__init__(name, lvl, hp)
        self.mp = mp

    def action(self):
        print(f"Маг {self.name} кастует заклинание! MP: {self.mp}")


class WarriorHero(Hero):
    def __init__(self, name, lvl, hp, weapon):
        super().__init__(name, lvl, hp)
        self.weapon = weapon

    def action(self):
        print(f"Воин {self.name} рубит {self.weapon}! Уровень: {self.lvl}")


# ==========================================
# 3. КЛАСС BANK ACCOUNT
# ==========================================

class BankAccount:
    def __init__(self, hero, balance, password, bank_name):
        self.hero = hero
        self._balance = balance
        self.__password = password
        self.bank_name = bank_name

    # Проверка пароля
    def login(self, password):
        return password == self.__password

    # Свойство только для чтения
    @property
    def full_info(self):
        return f"{self.hero.name} | Баланс: {self._balance} СОМ"

    # Название банка
    def get_bank_name(self):
        return self.bank_name

    # Бонус за уровень
    def bonus_for_level(self):
        return self.hero.lvl * 10

    # Магический метод __str__
    def __str__(self):
        return f"{self.hero.name} | Баланс: {self._balance} СОМ"

    # Магический метод __add__
    def __add__(self, other):
        if type(self.hero) is not type(other.hero):
            raise TypeError(
                "Нельзя сложить счета героев разных классов!"
            )

        return self._balance + other._balance

    # Магический метод __eq__
    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return False

        return (
            type(self.hero) is type(other.hero)
            and self.hero.lvl == other.hero.lvl
        )


# ==========================================
# 4. СОЗДАЁМ ГЕРОЕВ
# ==========================================

mage1 = MageHero(
    name="Merlin",
    lvl=50,
    hp=100,
    mp=150
)

mage2 = MageHero(
    name="Merlin",
    lvl=50,
    hp=100,
    mp=100
)

warrior1 = WarriorHero(
    name="Conan",
    lvl=50,
    hp=200,
    weapon="мечом"
)


# ==========================================
# 5. ПРОВЕРЯЕМ ACTION()
# ==========================================

mage1.action()

warrior1.action()


# ==========================================
# 6. СОЗДАЁМ БАНКОВСКИЕ СЧЕТА
# ==========================================

acc1 = BankAccount(
    hero=mage1,
    balance=5000,
    password="1234",
    bank_name="Simba"
)

acc2 = BankAccount(
    hero=mage2,
    balance=3000,
    password="5678",
    bank_name="Simba"
)

acc3 = BankAccount(
    hero=warrior1,
    balance=4000,
    password="9999",
    bank_name="Simba"
)


# ==========================================
# 7. ПРОВЕРКА __str__
# ==========================================

print(acc1)
print(acc2)


# ==========================================
# 8. ПРОВЕРКА LOGIN
# ==========================================

print("\n=== Проверка login ===")

print("Правильный пароль:", acc1.login("1234"))
print("Неправильный пароль:", acc1.login("0000"))


# ==========================================
# 9. FULL INFO
# ==========================================

print("\n=== Информация о счёте ===")

print(acc1.full_info)
print(acc2.full_info)


# ==========================================
# 10. БАНК
# ==========================================

print("\n=== Банк ===")

print("Банк:", acc1.get_bank_name())


# ==========================================
# 11. БОНУС ЗА УРОВЕНЬ
# ==========================================

print("\n=== Бонус ===")

print(
    "Бонус за уровень:",
    acc1.bonus_for_level(),
    "СОМ"
)


# ==========================================
# 12. ПРОВЕРКА __add__
# ==========================================

print("\n=== Проверка __add__ ===")

print(
    "Сумма счетов двух магов:",
    acc1 + acc2
)

try:
    print(
        "Сумма счёта мага и воина:",
        acc1 + acc3
    )
except TypeError as error:
    print("Ошибка:", error)


# ==========================================
# 13. ПРОВЕРКА __eq__
# ==========================================

print("\n=== Проверка __eq__ ===")

print(
    "Mage1 == Mage2 ?",
    acc1 == acc2
)

print(
    "Mage1 == Warrior ?",
    acc1 == acc3
)