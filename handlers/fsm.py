from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.main_db import add_category, add_product


router = Router()


class ProductForm(StatesGroup):
    category = State()
    product_name = State()
    price = State()


@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Чтобы добавить товар, напиши:\n"
        "Добавить товар"
    )


@router.message(lambda message: message.text and message.text.lower() == "добавить товар")
async def start_product(message: Message, state: FSMContext):
    await message.answer("Введите категорию товара:")
    await state.set_state(ProductForm.category)


@router.message(ProductForm.category)
async def get_category(message: Message, state: FSMContext):
    category_name = message.text

    category_id = add_category(category_name)

    await state.update_data(
        category_id=category_id,
        category_name=category_name
    )

    await message.answer("Введите название товара:")
    await state.set_state(ProductForm.product_name)


@router.message(ProductForm.product_name)
async def get_product_name(message: Message, state: FSMContext):
    await state.update_data(
        product_name=message.text
    )

    await message.answer("Введите цену товара числом, например: 6700")
    await state.set_state(ProductForm.price)


@router.message(ProductForm.price)
async def get_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer(
            "Введите цену числом, например: 6700"
        )
        return

    data = await state.get_data()

    add_product(
        data["product_name"],
        price,
        data["category_id"]
    )

    await message.answer(
        f"Товар сохранён! ✅\n\n"
        f"Категория: {data['category_name']}\n"
        f"Название: {data['product_name']}\n"
        f"Цена: {price}"
    )

    await state.clear()