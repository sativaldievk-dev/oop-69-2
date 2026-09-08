from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.database import add_product, get_products
from states.product import ProductState
from keyboards.main_buttons import main_buttons

router=Router()

@router.message(Command("add_product"))
async def add_start(message:Message,state:FSMContext):
    await state.set_state(ProductState.name)
    await message.answer("Введите название товара:")

@router.message(ProductState.name)
async def get_name(message:Message,state:FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Введите название товара текстом.")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(ProductState.price)
    await message.answer("Введите цену товара:")

@router.message(ProductState.price)
async def get_price(message:Message,state:FSMContext):
    if not message.text or not message.text.strip().isdigit():
        await message.answer("❌ Цена должна быть числом. Например: 150")
        return
    data=await state.get_data()
    price=int(message.text.strip())
    await add_product(data["name"],price)
    await state.clear()
    await message.answer(f"✅ Товар добавлен!\n{data['name']} — {price} сом",reply_markup=main_buttons)

@router.message(Command("drinks"))
async def drinks(message:Message):
    products=await get_products()
    if not products:
        await message.answer("Ничего пока нету.")
        return
    await message.answer("🥤 Товары:\n\n"+"\n".join(f"• {n} — {p} сом" for n,p in products))
