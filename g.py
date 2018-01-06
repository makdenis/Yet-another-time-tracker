"""
Created by anthony on 12.11.17
global variables shared across the app to prevent cyclic references
"""
import logging
import os

# TODO move config into configFile  in config.log_config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


log = logging.getLogger(__name__)


log.info('> Starting globals')

updater = None
queue = None
automata = None

TOKEN = os.environ['TOKEN']
BOT_ENV = os.environ['BOT_ENV']
log.info(f'BOT_ENV set to "{BOT_ENV}" mode')

dev_mode = 'dev' == BOT_ENV
prod_mode = 'prod' == BOT_ENV
test_mode = 'test' == BOT_ENV

log.info('Globals have started')
