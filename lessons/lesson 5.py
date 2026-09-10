# abstractmethod
# staticmethod
# classmethod
# property

def simple_decorator(func):
    def wrapper():
        print('До выполнения!!')
        func()
        print('после выполнения!!')
    return wrapper

@simple_decorator
def say_hello():
    print('Hello')

# say_hello()
def greeting_decorator(func):
    def wrapper(name):
        print(f"Привет {name}")
        func(name)
    return wrapper
@greeting_decorator
def greeting(name):
    print(f'Как дела {name}?')
# greeting("Ardager")

def repeat_decorator(value):
    def decorator(func):
        def wrapper(name):
            for i in range(value):
                func(name)
        return wrapper
    return decorator

@repeat_decorator(5)
def say_hello_world(name):
    print(f'{name} say hello world!!')

# say_hello_world('Ardager')


def class_decorator(cls):
    class NewClass(cls):
        def new_method(self):
            print('New method!!')

    return NewClass

@class_decorator
class OldClass:
    def old_method(self):
        print('Old method!!')

test_obj = OldClass()
# print(type(test_obj))
# test_obj.old_method()
# test_obj.new_method()

# import lesson1 as l
# from lesson1 import Hero

# ardager = Hero("Ardager", 110, 11000)
# ardager.action()