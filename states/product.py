from aiogram.fsm.state import State,StatesGroup

class ProductState(StatesGroup):
    name=State()
    price=State()
