
class BankAccount:

    def __init__(self, login, balance, password):
        self.login = login
        self._balance = balance
        self.__password = password

    def get_balance(self):
        print(self._balance)

    def method_login(self, password):
        if password == self.__password:
            return "OK"
        else:
            return "Не верный пароль!!"



ardager = BankAccount('ardger', 1000, "2638")
# print(ardager.method_login("2638"))

# print(ardager.login)
# print(ardager._balance)
# print(ardager.__dict__)
# ardager.get_pass()
# ardager.get_balance()




from abc import ABC, abstractmethod

# Абстрактный класс
class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass
    @abstractmethod
    def move(self):
        pass
class Dog(Animal):
    def make_sound(self):
        print("GAf GAF")
    def move(self):
        print("Step")
class Cat(Animal):
    def make_sound(self):
        print('May May')
    def move(self):
        print('STEPS')

gufi = Dog()
kiti = Cat()



class SendOTP(ABC):
    @abstractmethod
    def sent_otp_to_phone(self, phone):
        pass


class KG(SendOTP):
    def sent_otp_to_phone(self, phone):
        data = f'''
        <Phone>{phone}</Phone>
        <text>Ваш пароль: 1234</Text>
        '''
        print(data)

class RU(SendOTP):
    def sent_otp_to_phone(self, phone):
        data = {
            "Phone": phone,
            "Text": "Ваш пароль: 1234"
        }
        print(data)