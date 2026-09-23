from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "📚 Добро пожаловать в каталог книг!\n\n"
        "Используйте команду /add_book, чтобы добавить книгу.\n"
        "Используйте команду /books, чтобы посмотреть каталог."
    )