from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """Эхо хендлер который ловит сообщения без команд"""
    bot.reply_to(message, "Я тебя не понимаю, пользуйся кнопками📱")
