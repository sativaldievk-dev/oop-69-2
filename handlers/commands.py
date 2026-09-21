from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.database import get_products

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Команды:\n"
        "/add_product — добавить товар\n"
        "/products — показать товары\n"
        "/drinks — показать товары\n"
        "/cancel — отменить добавление"
    )


@router.message(Command("products"))
async def products(message: Message):
    rows = get_products()

    if not rows:
        await message.answer("Товаров пока нет.")
        return

    for product_id, name, price, photo_id, category_name in rows:
        caption = (
            f"🛍 <b>{name}</b>\n"
            f"💰 Цена: {price} сом\n"
            f"📂 Категория: {category_name}\n"
            f"🆔 ID: {product_id}"
        )

        if photo_id:
            await message.answer_photo(
                photo=photo_id,
                caption=caption,
                parse_mode="HTML"
            )
        else:
            await message.answer(
                caption,
                parse_mode="HTML"
            )


@router.message(Command("drinks"))
async def drinks(message: Message):
    # Та же выборка через INNER JOIN, как требует ДЗ.
    await products(message)
