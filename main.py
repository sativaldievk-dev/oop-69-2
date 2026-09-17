import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from database.main_db import create_tables
from handlers.fsm import router


async def main():
    create_tables()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    print("Бот запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())