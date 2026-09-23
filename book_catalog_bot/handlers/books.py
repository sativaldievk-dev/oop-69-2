import aiosqlite

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("books"))
async def books_handler(message: Message):
    async with aiosqlite.connect("database/books.db") as db:
        cursor = await db.execute(
            """
            SELECT book_id, title, author
            FROM books
            ORDER BY book_id
            """
        )

        books = await cursor.fetchall()
        await cursor.close()

    if not books:
        await message.answer(
            "📚 Каталог книг пока пуст.\n\n"
            "Используйте /add_book, чтобы добавить книгу."
        )
        return

    text = "📚 <b>Каталог книг:</b>\n\n"

    for book_id, title, author in books:
        text += (
            f"📖 <b>№ {book_id}</b>\n"
            f"📕 Название: {title}\n"
            f"✍️ Автор: {author}\n\n"
        )

    await message.answer(text, parse_mode="HTML")