import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
# НАСТРОЙКА
# =========================================================

TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН_ОТ_BOTFATHER"


# =========================================================
# ЛОГИ
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# =========================================================
# КНОПКИ
# =========================================================

def main_keyboard():
    keyboard = [
        ["👋 Привет", "ℹ️ Помощь"],
        ["📞 Контакты", "🤖 О боте"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# =========================================================
# /START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    name = user.first_name if user.first_name else "друг"

    await update.message.reply_text(
        f"Привет, {name}! 👋\n\n"
        "Добро пожаловать в моего Telegram-бота! 🤖\n\n"
        "Выбери нужную кнопку ниже 👇",
        reply_markup=main_keyboard()
    )


# =========================================================
# /HELP
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "ℹ️ Помощь\n\n"
        "/start — запустить бота\n"
        "/help — показать помощь\n\n"
        "Также можешь использовать кнопки "
        "внизу экрана."
    )


# =========================================================
# КНОПКА "ПРИВЕТ"
# =========================================================

async def hello(update: Update):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Рад тебя видеть! 😎"
    )


# =========================================================
# КНОПКА "ПОМОЩЬ"
# =========================================================

async def help_button(update: Update):
    await update.message.reply_text(
        "ℹ️ Что умеет бот?\n\n"
        "• Отвечает на сообщения\n"
        "• Показывает информацию\n"
        "• Имеет удобное меню\n"
        "• Готов к дальнейшему развитию 🚀"
    )


# =========================================================
# КНОПКА "КОНТАКТЫ"
# =========================================================

async def contacts(update: Update):
    await update.message.reply_text(
        "📞 Контакты\n\n"
        "Телефон: +996 XXX XXX XXX\n"
        "Telegram: @your_username\n\n"
        "Здесь позже можно поставить свои настоящие контакты."
    )


# =========================================================
# КНОПКА "О БОТЕ"
# =========================================================

async def about(update: Update):
    await update.message.reply_text(
        "🤖 О боте\n\n"
        "Это Telegram-бот, созданный на Python.\n\n"
        "Версия: 1.0\n"
        "Язык: Python 🐍"
    )


# =========================================================
# ОБЫЧНЫЕ СООБЩЕНИЯ
# =========================================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    if text == "👋 Привет":
        await hello(update)

    elif text == "ℹ️ Помощь":
        await help_button(update)

    elif text == "📞 Контакты":
        await contacts(update)

    elif text == "🤖 О боте":
        await about(update)

    else:
        await update.message.reply_text(
            f"Ты написал:\n\n"
            f"«{text}»\n\n"
            "🤖 Я получил твоё сообщение!"
        )


# =========================================================
# ЗАПУСК БОТА
# =========================================================

def main():
    if TOKEN == "ВСТАВЬ_СЮДА_ТОКЕН_ОТ_BOTFATHER":
        print("❌ Ошибка!")
        print("Вставь токен от BotFather в переменную TOKEN.")
        return

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # Команды
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    # Обычные сообщения
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("================================")
    print("🤖 TELEGRAM БОТ ЗАПУЩЕН")
    print("================================")
    print("Бот работает...")
    print("Чтобы остановить бота: Ctrl + C")

    application.run_polling()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
