from database.db import return_history
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message


def history_keyboard_main(message: Message) -> InlineKeyboardMarkup:
    """Функция которая возвращает инлайн клавиатуру с историей поиска"""
    user_id = message.chat.id
    return_history(user_id)
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton("Дата поиска", callback_data="btn"),
               InlineKeyboardButton("Название", callback_data="btn"),
               InlineKeyboardButton("Ccылка", callback_data="btn"))
    if 0 < len(return_history(user_id)) < 10:
        for i in range(len(return_history(user_id))):
            markup.add(InlineKeyboardButton(f"{return_history(user_id)[i][1]}", callback_data="btn"),
                       InlineKeyboardButton(f"{return_history(user_id)[i][2]}", callback_data="btn"),
                       InlineKeyboardButton(f"{return_history(user_id)[i][3]}", url=f"{return_history(user_id)[i][3]}"))
    elif len(return_history(user_id)) > 9:
        for i in range(10):
            markup.add(InlineKeyboardButton(f"{return_history(user_id)[i][1]}", callback_data="btn"),
                       InlineKeyboardButton(f"{return_history(user_id)[i][2]}", callback_data="btn"),
                       InlineKeyboardButton(f"{return_history(user_id)[i][3]}", url=f"{return_history(user_id)[i][3]}"))
    else:
        markup.add(InlineKeyboardButton("История пустая", callback_data="but_1"))
    return markup
