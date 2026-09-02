import telebot
from datetime import datetime
import random

TOKEN = "7952976866:AAE0kceFslIYWIWseDQhMr_w5tUXaVb8RRU"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я твой бот 🤖\n\nНапиши /help, чтобы увидеть команды."
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "/time — текущая дата и время\n"
        "/random — случайное число от 1 до 100\n"
        "/joke — случайная шутка"
    )


@bot.message_handler(commands=['time'])
def get_time(message):
    now = datetime.now()
    bot.send_message(
        message.chat.id,
        f"Сейчас: {now.strftime('%d.%m.%Y %H:%M')}"
    )


@bot.message_handler(commands=['random'])
def get_random(message):
    number = random.randint(1, 100)
    bot.send_message(
        message.chat.id,
        f"Твоё случайное число: {number}"
    )


@bot.message_handler(commands=['joke'])
def get_joke(message):
    jokes = [
        "Почему программисты любят тёмную тему? Потому что свет притягивает баги 😄",
        "Программист превращает кофе в код ☕",
        "Баг — это незапланированная функция 😂",
        "Работает — не трогай 😎",
        "Python спросили: ты змея? Он ответил: я язык 🐍"
    ]

    joke = random.choice(jokes)
    bot.send_message(message.chat.id, joke)


bot.polling(none_stop=True)