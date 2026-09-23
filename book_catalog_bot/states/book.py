from aiogram.fsm.state import State, StatesGroup


class BookForm(StatesGroup):
    number = State()
    title = State()
    author = State()
    genre = State()