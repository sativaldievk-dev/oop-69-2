from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.main_db import delete_product
from keyboards.main_buttons import confirm_delete_keyboard


router = Router()


@router.callback_query(F.data.startswith("delete:"))
async def delete_start(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[1])

    await state.update_data(product_id=product_id)
    await callback.message.answer(
        "⚠️ Вы точно хотите удалить этот товар?",
        reply_markup=confirm_delete_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "delete_confirm")
async def delete_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")

    if product_id is None:
        await callback.message.answer("❌ Товар не найден.")
        await state.clear()
        await callback.answer()
        return

    deleted = delete_product(product_id)

    if deleted:
        await callback.message.answer("✅ Товар успешно удалён.")
    else:
        await callback.message.answer("❌ Не удалось удалить товар.")

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "delete_cancel")
async def delete_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Удаление отменено.")
    await callback.answer()