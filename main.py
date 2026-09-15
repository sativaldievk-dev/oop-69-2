import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from database.db import create_table
from database.queries import add_user, get_all_users

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Не найден BOT_TOKEN в файле .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n"
        "Заполни анкету командой /form\n"
        "Посмотреть все анкеты: /users"
    )


@dp.message(Command("form"))
async def form_start(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Как тебя зовут?")


@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")


@dp.message(Form.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введи возраст числом.")
        return

    age = int(message.text)

    if age < 1 or age > 120:
        await message.answer("Возраст должен быть от 1 до 120.")
        return

    await state.update_data(age=age)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Мужской"),
                KeyboardButton(text="Женский")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await state.set_state(Form.gender)
    await message.answer("Выбери пол:", reply_markup=keyboard)


@dp.message(Form.gender)
async def get_gender(message: Message, state: FSMContext):
    if message.text not in ["Мужской", "Женский"]:
        await message.answer("Выбери: Мужской или Женский.")
        return

    await state.update_data(gender=message.text)
    data = await state.get_data()

    add_user(
        name=data["name"],
        age=data["age"],
        gender=data["gender"]
    )

    await message.answer(
        "✅ Анкета сохранена в базе данных!\n\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Пол: {data['gender']}"
    )

    await state.clear()


@dp.message(Command("users"))
async def users(message: Message):
    users_list = get_all_users()

    if not users_list:
        await message.answer("📭 В базе пока нет записей.")
        return

    text = "📋 Все анкеты:\n\n"

    for user_id, name, age, gender in users_list:
        text += (
            f"ID: {user_id}\n"
            f"Имя: {name}\n"
            f"Возраст: {age}\n"
            f"Пол: {gender}\n"
            "────────────\n"
        )

    await message.answer(text)


@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Заполнение анкеты отменено.")


async def main():
    create_table()
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
