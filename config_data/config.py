from os import getenv
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()


BOT_TOKEN = getenv('BOT_TOKEN')
RAPID_API_KEY = getenv('RAPID_API_KEY')
NASA_KEY = getenv("NASA_KEY")


DEFAULT_COMMANDS = (
    ("start", "Основное меню"),
    ("help", "Вывести справку"),
    ("history", "История поиска")
)
