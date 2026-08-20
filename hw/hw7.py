from faker import Faker

# Эта библиотека нужна для генерации случайных данных:
# имён, email и адресов.
fake = Faker()

print("=== Внешняя библиотека Faker ===")

for i in range(5):
    print("Имя:", fake.name())
    print("Email:", fake.email())
    print("Адрес:", fake.address())
    print()


# Эта часть решает задачу Two Sum.
# Нужно найти два числа, сумма которых равна target.

print("=== Two Sum ===")

nums = [2, 7, 11, 15]
target = 9

# Первый цикл выбирает первое число.
for i in range(len(nums)):

    # Второй цикл выбирает второе число.
    for j in range(i + 1, len(nums)):

        if nums[i] + nums[j] == target:
            print("Результат:", [i, j])
            print(f"{nums[i]} + {nums[j]} = {target}")