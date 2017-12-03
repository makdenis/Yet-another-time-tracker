
"""
Created by anthony on 15.10.17
Main bot file
Only _register_ modules here (no logic)
Should just assemble and run bot
"""
from telegram.ext import Updater
import logging
from telegram.ext import CallbackQueryHandler
from components.automata import Automata
from config import bot_config
import handlers.interaction_handler
import services.state_service
from config.db_config import init_db
import g


log = logging.getLogger(__name__)


def init_job_queue():
    log.info('> Starting job queue')
    g.updater = Updater(token=bot_config.BOT_API_TOKEN)
    g.queue = g.updater.job_queue
    log.info('Job queue has started')


def init_automata():
    log.info('> Starting automata')
    g.automata = Automata()
    log.info('Automata has started')


def init_bot():
    log.info(f'> Starting {bot_config.BOT_NAME}')

    # registers handlers
    dispatcher = g.updater.dispatcher

    # handlers are invoked till the first match
    dispatcher.add_handler(handlers.interaction_handler.command_handler())
    dispatcher.add_handler(CallbackQueryHandler(services.state_service.button))
    # runs
    g.updater.start_polling()
    log.info('Bot has started')

    # listens for Ctrl-C on process to stop
    g.updater.idle()
    log.info('Bot has stopped')


def main():
    # TODO handle startup error
    init_db()
    init_job_queue()
    init_automata()
    init_bot()


if __name__ == '__main__':
    main()
