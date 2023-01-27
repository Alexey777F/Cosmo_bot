from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard() -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру с кнопками"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('/🌌Галактики🌌')
    btn2 = KeyboardButton('/🌕Марс🌕')
    keyboard.add(btn1).row(btn2)
    return keyboard