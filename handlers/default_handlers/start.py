from telebot.types import Message
from loader import bot
from keyboards.reply.keyboard import keyboard


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
        """Хендлер который вызывается при команде старт"""
        bot.send_message(chat_id=message.chat.id,
                    text=f"Привет {message.from_user.first_name}👋\n\n"
                    f"Покажу красивые фото🌌\n\n"
                    "Для справки обратитесь в раздел /help❓\n\n"
                    "История в разделе /history🔎\n\n"
                    "Выбери интересующий раздел🎆",
                    reply_markup=keyboard())