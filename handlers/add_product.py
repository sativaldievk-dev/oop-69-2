from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.database import add_product, get_or_create_category
from states.product import ProductState

router = Router()


@router.message(Command("add_product"))
async def add_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ProductState.name)
    await message.answer("Введите название товара:")


@router.message(ProductState.name)
async def get_name(message: Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("❌ Введите название товара текстом.")
        return

    await state.update_data(name=message.text.strip())
    await state.set_state(ProductState.price)
    await message.answer("Введите цену товара:")


@router.message(ProductState.price)
async def get_price(message: Message, state: FSMContext):
    if not message.text or not message.text.strip().isdigit():
        await message.answer("❌ Цена должна быть числом. Например: 1500")
        return

    price = int(message.text.strip())

    await state.update_data(price=price)
    await state.set_state(ProductState.category)
    await message.answer("Введите категорию товара:")


@router.message(ProductState.category)
async def get_category(message: Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("❌ Введите название категории.")
        return

    category_id = get_or_create_category(message.text.strip())

    await state.update_data(category_id=category_id)
    await state.set_state(ProductState.photo)
    await message.answer("Теперь отправьте ФОТО товара 📸")


@router.message(ProductState.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    # Telegram хранит фотографию у себя.
    # В базу записываем только короткий file_id.
    photo_id = message.photo[-1].file_id

    data = await state.get_data()

    add_product(
        name=data["name"],
        price=data["price"],
        category_id=data["category_id"],
        photo_id=photo_id,
    )

    await message.answer(
          f"✅ Товар добавлен!\n"
          f"Название: {data['name']}\n"
          f"Цена: {data['price']} сом\n"
          f"Фото: сохранено"
    )

    await state.clear()



@router.message(ProductState.photo)
async def photo_required(message: Message):
    await message.answer("❌ Нужно отправить именно фотографию 📸")


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Добавление товара отменено.")
