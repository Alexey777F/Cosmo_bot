from telebot.types import Message
from loader import bot
from telegram_bot_calendar import DetailedTelegramCalendar
import datetime
from utils.calendars import translate_y_m_d
from loader import nasa_key, mars_url
from api.request import get_response, get_json, get_mars_data, information
from handlers.custom_handlers.handler_db import return_database


@bot.message_handler(commands=["🌕Марс🌕"])
def check_in_calendar(message: Message) -> None:
    """Хендлер который ловит команду Марс создает календарь"""
    calendar, step = DetailedTelegramCalendar(calendar_id=2,
                                              min_date=datetime.date(2014, 2, 1),
                                              max_date=datetime.date.today()).build()
    bot.send_message(message.from_user.id, f"Выберите дату из календаря\n\n"
                                           f"Выберите {translate_y_m_d()[step]}📆",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def check_in(call):
    """Колбек хендлер который берет значения выбранной даты из календаря"""
    """и передает в request для запроса через api возвращая данные с сайта и отправляя пользователю"""
    result, key, step = DetailedTelegramCalendar(calendar_id=2, locale="ru",
                                                 min_date=datetime.date(2014, 2, 1),
                                                 max_date=datetime.date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату из календаря\n\n"
                              f"Выберите {translate_y_m_d()[step]}📆",
                              call.message.chat.id, call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(text=f"Вы выбрали {result.strftime('%d-%m-%Y')}📆\nПеревожу страничку, секундочку...🖌",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        response = get_response(mars_url(result, nasa_key))
        if response is not None:
            json = get_json(get_response(mars_url(result, nasa_key)))["photos"]
            if len(json) == 0 or "img_src" not in json[0].keys():
                bot.edit_message_text(
                    text=f"На дату {result} фотографий не найдено. Повторите поиск",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id)
            else:
                data = get_mars_data(get_json(get_response(mars_url(result, nasa_key))))
                bot.edit_message_text(text=f"Вы выбрали дату {result.strftime('%d-%m-%Y')}📆\n\n"
                                           f"{information()}\n\n{data}",
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
                return_database(call, 'Марс', str(result.strftime('%d-%m-%Y')),
                                "Фото с марса",
                                f"{data}")
        else:
            bot.edit_message_text(text=f"Нет данных на сервере на {result}, повторите запрос позже или выберите другую дату",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)