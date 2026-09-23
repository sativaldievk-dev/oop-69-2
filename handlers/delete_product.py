from aiogram import Router, F
from aiogram.types import Message

from database.main_db import delete_product

router = Router()


@router.message(F.text.startswith("/delete"))
async def delete_product_handler(message: Message):
    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Используй: /delete ID")
        return

    try:
        product_id = int(parts[1])
    except ValueError:
        await message.answer("ID товара должен быть числом.")
        return

    deleted = delete_product(product_id)

    if deleted:
        await message.answer(f"Товар с ID {product_id} удалён.")
    else:
        await message.answer(f"Товар с ID {product_id} не найден.")
