import aiosqlite
from aiogram import Router 
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.book import BookForm

router = Router()


@router.message(Command("add_book"))
async def add_book_handler(message: Message, state: FSMContext):
    await state.set_state(BookForm.number)

    await message.answer(
        "📚 Добавление книги\n\n"
        "Шаг 1 из 4\n"
        "Введите номер книги:"
    )


@router.message(BookForm.number)
async def book_number_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            "❌ Нужно ввести число.\n"
            "Попробуйте ещё раз:"
        )
        return

    await state.update_data(number=int(message.text))
    await state.set_state(BookForm.title)

    await message.answer(
        "Шаг 2 из 4\n"
        "Введите название книги:"
    )


@router.message(BookForm.title)
async def book_title_handler(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(BookForm.author)

    await message.answer(
        "Шаг 3 из 4\n"
        "Введите автора книги:"
    )


@router.message(BookForm.author)
async def book_author_handler(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(BookForm.genre)

    await message.answer(
        "Шаг 4 из 4\n"
        "Введите жанр книги:"
    )


@router.message(BookForm.genre)
async def book_genre_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    number = data["number"]
    title = data["title"]
    author = data["author"]
    genre = message.text

    try:
        async with aiosqlite.connect("database/books.db") as db:

            await db.execute(
                """
                INSERT INTO books (book_id, title, author)
                VALUES (?, ?, ?)
                """,
                (number, title, author)
            )

            await db.execute(
                """
                INSERT INTO books_detail (book_id, genre)
                VALUES (?, ?)
                """,
                (number, genre)
            )

            await db.commit()

        await message.answer(
            "✅ Книга сохранена!\n\n"
            f"📖 Номер: {number}\n"
            f"📚 Название: {title}\n"
            f"✍️ Автор: {author}\n"
            f"🏷 Жанр: {genre}"
        )

    except aiosqlite.IntegrityError:
        await message.answer(
            "❌ Книга с таким номером уже существует."
        )

    await state.clear()