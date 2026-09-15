import random
#
# def random_games():
#     secret_number = random.randint(1, 100)
#     attempts_count = 0
#     print("Я загадал число от 1 до 100. У вас есть 8 попыток")
#
#     while attempts_count < 8:
#         user_number = int(input("Ваше число: "))
#         attempts_count += 1
#
#         if user_number < secret_number:
#             print(f"Загаданное число БОЛЬШЕ чем {user_number}")
#         elif user_number > secret_number:
#             print(f"Загаданное число МЕНЬШЕ чем {user_number}")
#         else:
#             print(f"ПОЗДРАВЛЯЮ! Вы угадали число {secret_number} за {attempts_count} попыток!")
#             break
#     else:
#         print(f"Вы не уложились за 8 попыток. Я загадал число {secret_number}")
#
#
# random_games()
from traceback import print_tb


# def get_first(dict_1):
#     return dict_1["name"]
#
#
# print(get_first({"name": "Bektur", "age": 11}))


# def find_max(list_1):
#     max_val = list_1[0]
#     for i in list_1:
#         if i > max_val:
#             max_val = i
#     return max_val
#
#
# print(find_max([i for i in range(1500)]))


def has_duplicates(list_duplicates):
    len_list = len(list_duplicates)
    for i in range(len_list):
        for j in range(i + 1, len_list):
            if list_duplicates[i] == list_duplicates[j]:
                return True
    return False

print(has_duplicates([1, 2, 3, 4, 5]))

# list_numbers = [1,2,3]
#
# for i in list_numbers: print(i)
#
# for i in list_numbers:
#     for j in list_numbers:
#         print(i,j)
#
# list_numbers[0]