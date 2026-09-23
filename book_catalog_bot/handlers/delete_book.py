import aiosqlite

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("delete"))
async def delete_book_handler(message: Message):
    await message.answer(
        "🗑 Удаление книги\n\n"
        "Введите номер книги:"
    )


@router.message()
async def delete_book_number(message: Message):
    if message.text and message.text.isdigit():
        number = int(message.text)

        async with aiosqlite.connect("database/books.db") as db:
            cursor = await db.execute(
                "SELECT title FROM books WHERE book_id = ?",
                (number,)
            )
            book = await cursor.fetchone()

            if not book:
                await message.answer(
                    "❌ Книга с таким номером не найдена."
                )
                return

            await db.execute(
                "DELETE FROM books_detail WHERE book_id = ?",
                (number,)
            )

            await db.execute(
                "DELETE FROM books WHERE book_id = ?",
                (number,)
            )

            await db.commit()

        await message.answer(
            f"✅ Книга «{book[0]}» удалена!"
        )