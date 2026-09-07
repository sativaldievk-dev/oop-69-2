import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# =========================
# ТОКЕН БОТА
# =========================

TOKEN = getenv("")

# Если переменная BOT_TOKEN не настроена,
# можешь временно написать токен прямо сюда:
# TOKEN = getenv("8697925618:AAEQc8RUQs4iWXUrBi7lToT5e0E9nS3v1SE")

TOKEN = "8697925618:AAEQc8RUQs4iWXUrBi7lToT5e0E9nS3v1SE"


# =========================
# ROUTER
# =========================

router = Router()


# =========================
# СОСТОЯНИЯ АНКЕТЫ (FSM)
# =========================

class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()


# =========================
# /start
# =========================

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(Form.name)

    await message.answer(
        "👋 Привет!\n\n"
        "Давай заполним анкету.\n"
        "Как тебя зовут?"
    )


# =========================
# /form
# =========================

@router.message(Command("form"))
async def form_handler(message: Message, state: FSMContext):
    await state.set_state(Form.name)

    await message.answer(
        "📝 Начинаем анкету!\n\n"
        "Как тебя зовут?"
    )


# =========================
# ИМЯ
# =========================

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):

    if not message.text:
        await message.answer("Пожалуйста, напиши имя текстом.")
        return

    await state.update_data(name=message.text)

    await state.set_state(Form.age)

    await message.answer(
        "Отлично 👍\n"
        "Теперь напиши свой возраст."
    )


# =========================
# ВОЗРАСТ
# =========================

@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):

    if not message.text or not message.text.isdigit():
        await message.answer(
            "❗ Возраст должен быть числом.\n"
            "Например: 16"
        )
        return

    age = int(message.text)

    if age <= 0 or age > 120:
        await message.answer(
            "❗ Введи реальный возраст числом."
        )
        return

    await state.update_data(age=age)

    await state.set_state(Form.gender)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Мужской"),
                KeyboardButton(text="Женский"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer(
        "Теперь выбери пол:",
        reply_markup=keyboard
    )


# =========================
# ПОЛ
# =========================

@router.message(Form.gender, F.text.in_(["Мужской", "Женский"]))
async def process_gender(message: Message, state: FSMContext):

    await state.update_data(gender=message.text)

    data = await state.get_data()

    name = data["name"]
    age = data["age"]
    gender = data["gender"]

    # Очищаем состояние после окончания анкеты
    await state.clear()

    await message.answer(
        "✅ Анкета заполнена!\n\n"
        f"👤 Имя: {name}\n"
        f"🎂 Возраст: {age}\n"
        f"⚧ Пол: {gender}",
        reply_markup=ReplyKeyboardRemove()
    )


# =========================
# НЕПРАВИЛЬНЫЙ ПОЛ
# =========================

@router.message(Form.gender)
async def wrong_gender(message: Message):

    await message.answer(
        "Пожалуйста, выбери один из вариантов:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Мужской"),
                    KeyboardButton(text="Женский"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    )


# =========================
# /cancel
# =========================

@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:
        await message.answer(
            "Сейчас анкета не заполняется."
        )
        return

    await state.clear()

    await message.answer(
        "❌ Анкета отменена.",
        reply_markup=ReplyKeyboardRemove()
    )


# =========================
# ЗАПУСК БОТА
# =========================

async def main():

    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout
    )

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()

    dp.include_router(router)

    print("Бот запущен!")

    await dp.start_polling(bot)


# =========================
# START
# =========================

if __name__ == "__main__":
    asyncio.run(main())