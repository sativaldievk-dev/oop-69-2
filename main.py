import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.database import create_tables
from handlers.start import router as start_router
from handlers.add_book import router as add_book_router
from handlers.books import router as books_router


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не найден в .env")
        return

    create_tables()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(add_book_router)
    dp.include_router(books_router)

    print("Бот запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())