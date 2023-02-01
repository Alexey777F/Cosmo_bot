from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
nasa_key = config.NASA_KEY


def cosmo_url(key, result):
    url = f"https://api.nasa.gov/planetary/apod?api_key={key}&start_date={result}&end_date={result}"
    return url


def mars_url(result, key):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={result}&api_key={key}"
    return url