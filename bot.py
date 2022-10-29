import os
import sys
import logging

from telegram import Bot
from telegram.ext import Updater

import handlers

logging.basicConfig(level=logging.INFO, format='[ %(asctime)s ] [ %(name)s ] [ %(levelname)s ]  { %(message)s },')

token_env_name = os.getenv('TOKEN_ENV_NAME',None)
if token_env_name is None:
    token_env_name = 'TOKEN'

env_vars = [token_env_name, 'revisionchat', 'mainchannel']

## check that required environment variables exists
for var in env_vars:    
    if os.getenv(var, None) is None:
        print(f'`{var}` environment variable missing', file = sys.stderr)
        exit(1)

TOKEN = os.getenv(token_env_name)

dimension_bot = Bot(token=TOKEN)

updater = Updater(bot=dimension_bot)
dispatcher = updater.dispatcher

dispatcher.add_handler(handlers.conv_handler)
dispatcher.add_handler(handlers.process_artwork_handler)

updater.start_polling()
print('BOT running with long polling',file=sys.stderr,flush=True)
updater.idle()
