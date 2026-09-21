import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.database import create_tables
from handlers.add_product import router as add_product_router
from handlers.commands import router as commands_router
from handlers.echo import router as echo_router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в файле .env")

    create_tables()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(commands_router)
    dp.include_router(add_product_router)
    dp.include_router(echo_router)

    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
