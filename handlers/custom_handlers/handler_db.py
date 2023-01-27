from database import db
import datetime


def return_database(message, btn_name, calendar_date, name, link) -> None:
    """Функция которая записывает данные в бд"""
    db.init_db()
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    today = datetime.datetime.today()
    date = today.strftime("%d.%m.%Y %H:%M")
    user_id = message.from_user.id
    btn = btn_name
    calendar_date = calendar_date
    title = name
    link = link
    return db.user_info(first_name, last_name, date, user_id, btn, calendar_date, title, link)
