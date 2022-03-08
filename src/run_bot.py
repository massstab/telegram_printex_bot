import logging
from telegram.ext import Updater
from handlers import SmallHandler
from configparser import ConfigParser


def get_token():
    config = ConfigParser()
    config.read('config.cfg')
    return config.get('auth', 'token')

def get_own_id():
    config = ConfigParser()
    config.read('config.cfg')
    id = config.get('auth', 'own_id')
    return int(id)

if __name__ == '__main__':
    token = get_token()
    own_id =get_own_id()
    keywords = ['/tex', '/logfile']
    logging.basicConfig(filename='logfile.txt', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    small_handlers = SmallHandler(updater, dispatcher, own_id, token)

    small_handlers.start_message()
    small_handlers.logfile_sender()
    small_handlers.texify()

    small_handlers.updater.start_polling(timeout=100)