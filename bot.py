
"""
Created by anthony on 15.10.17
Main bot file
Only _register_ modules here (no logic)
Should just assemble and run bot
"""
from telegram.ext import Updater
import logging
import time

from components.automata import Automata
from handlers import interaction_handler
from config.db_config import init_db
import g
from services import notification_service


log = logging.getLogger(__name__)


def init_job_queue():
    log.info('> Starting job queue')
    g.updater = Updater(token=g.TOKEN)
    g.queue = g.updater.job_queue
    log.info('Loading notification jobs')
    notification_service.load_tasks_to_queue()
    log.info('Job queue has started')


def init_automata():
    log.info('> Starting automata')
    g.automata = Automata()
    log.info('Automata has started')


def init_bot():
    log.info(f'> Starting bot')

    # registers handlers
    dispatcher = g.updater.dispatcher

    # handlers are invoked till the first match
    dispatcher.add_handler(interaction_handler.command_handler())
    dispatcher.add_handler(interaction_handler.callback_handler())
    # runs
    g.updater.start_polling()
    log.info('Bot has started')

    # listens for Ctrl-C on process to stop
    g.updater.idle()
    log.info('Bot has stopped')


def main():
    if g.prod_mode:
        delay = 15
        log.info(f'Waiting {delay} seconds before start up')
        time.sleep(delay)

    # TODO handle startup error
    init_db()
    init_job_queue()
    init_automata()
    init_bot()


if __name__ == '__main__':
    main()
