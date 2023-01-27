from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
nasa_key = config.NASA_KEY
