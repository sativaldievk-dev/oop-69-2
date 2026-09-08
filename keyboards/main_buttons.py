from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton

main_buttons=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/menu")],
        [KeyboardButton(text="/add_product"),KeyboardButton(text="/drinks")]
    ],resize_keyboard=True)

about_keyboard=InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="ℹ️ О нас",callback_data="about")]]
)
