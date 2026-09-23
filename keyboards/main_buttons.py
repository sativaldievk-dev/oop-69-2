from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton

main_buttons=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/menu")],
        [KeyboardButton(text="/add_product"),KeyboardButton(text="/drinks")]
    ],resize_keyboard=True)

about_keyboard=InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="ℹ️ О нас",callback_data="about")]]
)
def confirm_delete_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да, удалить",
                    callback_data="delete_confirm"
                ),
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="delete_cancel"
                )
            ]
        ]
    )