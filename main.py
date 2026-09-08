import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from database.database import create_db
from handlers.commands import router as commands_router
from handlers.add_product import router as product_router
from handlers.echo import router as echo_router

async def main():
    await create_db()
    bot=Bot(token=TOKEN)
    dp=Dispatcher()
    dp.include_router(commands_router)
    dp.include_router(product_router)
    dp.include_router(echo_router)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
