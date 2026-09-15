from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.main_buttons import main_buttons, about_keyboard

router=Router()

@router.message(Command("start"))
async def start(message:Message):
    await message.answer("☕ Добро пожаловать в кафе!\nНажми /menu.",reply_markup=main_buttons)

@router.message(Command("menu"))
async def menu(message:Message):
    await message.answer(
        "📋 Команды:\n/start — запуск\n/menu — меню\n/add_product — добавить товар\n/drinks — товары",
        reply_markup=about_keyboard)

@router.callback_query(F.data=="about")
async def about(callback:CallbackQuery):
    await callback.answer()
    await callback.message.answer("ℹ️ О нас\n\nМы — уютное кафе с вкусными напитками.")
