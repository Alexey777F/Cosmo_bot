from telebot.types import Message
from loader import bot
from telegram_bot_calendar import DetailedTelegramCalendar
import datetime
from utils.calendars import translate_y_m_d
from loader import nasa_key
from api.request_galaxy import get_response, get_json, get_data
from handlers.custom_handlers.handler_db import return_database


@bot.message_handler(commands=["🌌Галактики🌌"])
def check_in_calendar(message: Message) -> None:
    """Хендлер который ловит команду Галактики и создает календарь"""
    calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                              min_date=datetime.date(1996, 1, 2),
                                              max_date=datetime.date.today()).build()
    bot.send_message(message.from_user.id,
                     f"Выберите дату из календаря\n\nВыберите {translate_y_m_d()[step]}📆",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def check_in(call):
    """Колбек хендлер который берет значения выбранной даты из календаря"""
    """и передает в request для запроса через api"""
    """Возвращаeт данные с сайта и отправляет пользователю"""
    result, key, step = DetailedTelegramCalendar(calendar_id=1, locale="ru",
                                                 min_date=datetime.date(1996, 1, 2),
                                                 max_date=datetime.date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату из календаря\n\nВыберите {translate_y_m_d()[step]}📆",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(text=f"Вы выбрали {result.strftime('%d-%m-%Y')}📆\nПеревожу страничку, секундочку...🖌",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        if get_response(nasa_key, result) != None:
            print("Request is OK")
            if len(get_json(get_response(nasa_key, result))[0]) > 0:
                bot.edit_message_text(text=f"Вы выбрали дату {result.strftime('%d-%m-%Y')}📆\n\n"
                                           f"{get_data(get_json(get_response(nasa_key, result)))['Галактика']}\n\n"
                                           f"{get_data(get_json(get_response(nasa_key, result)))['Ссылка']}\n\n"
                                           f"{get_data(get_json(get_response(nasa_key, result)))['Описание']}",
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
                return_database(call, 'Галактики', str(result.strftime('%d-%m-%Y')),
                                f"{get_data(get_json(get_response(nasa_key, result)))['Галактика']}",
                                f"{get_data(get_json(get_response(nasa_key, result)))['Ссылка']}")
            else:
                bot.edit_message_text(
                    text=f"На дату {result.strftime('%d-%m-%Y')} фотографий не найдено. Повторите поиск",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id)
        else:
            print("NOT")
            bot.edit_message_text(text=f"Нет данных на сервере на {result.strftime('%d-%m-%Y')}, повторите запрос позже или выберите другую дату",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)