from loader import bot
from utils.set_bot_commands import set_default_commands
from handlers.default_handlers import start
import logging
import datetime
import time


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("start bot")
    set_default_commands(bot)
    while True:
        try:
            bot.polling(none_stop=True, timeout=90)
        except Exception as e:
            logger.error(datetime.datetime.now(), e)
            time.sleep(5)
            continue