from telebot.types import Message
from loader import bot
from keyboards.inline.history_keyboard import history_keyboard_main


@bot.message_handler(commands=["history"])
def bot_history(message: Message) -> None:
    """Хендлер который возвращает историю поиска"""
    bot.send_message(chat_id=message.chat.id, text="История: 📜", reply_markup=history_keyboard_main(message))
