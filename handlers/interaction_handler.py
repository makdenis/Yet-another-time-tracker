"""
Created by anthony on 15.10.17
start_handler
"""
import json
import logging

import datetime
from emoji import emojize
from telegram import ParseMode
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler

import g
from components.automata import CONTEXT_COMMANDS, CONTEXT_TASK, CONTEXT_LANG, CONTEXT_ACTION
from components.filter import command_filter
from components.message_source import message_source
from config.state_config import CallbackData, Language, ADMINS
from services import state_service
from utils.handler_utils import get_command_type, is_callback, deserialize_data


log = logging.getLogger(__name__)


def command_handler():
    return MessageHandler(Filters.all, handle)


def callback_handler():
    return CallbackQueryHandler(callback=handle)


ERR_COUNTER = {}


def handle(bot, update):
    chat = update.effective_chat
    chat_id = chat.id
    curr_context = None
    try:
        curr_command = None
        curr_action = None
        if is_callback(update):
            # Callback handling
            log.info(f'--> Callback from {chat.username} ({chat.id})')

            data = update.callback_query.data
            deserialized = deserialize_data(update.callback_query.data)

            curr_command = deserialized[CallbackData.COMMAND]
            curr_action = deserialized[CallbackData.ACTION]

        else:
            # Regular message/command handling
            log.info(f'--> Message from {chat.username} ({chat.id})')
            text = update.message.text

            if command_filter.known_command(text) is False:
                # check if user is admin
                if chat_id in ADMINS and '/stats' == text:
                    bot.send_message(chat_id=chat_id, text=json.dumps(ERR_COUNTER, indent=2))
                    return

                reply_on_unknown(bot, chat_id)
                return

            curr_command = get_command_type(text)

        # get all params needed to render state
        curr_state = g.automata.get_state(chat_id)
        curr_context = g.automata.get_context(chat_id)
        log.info(f'curr_state: {curr_state}, curr_command: {curr_command}')


        # find out state to be rendered
        next_state = g.automata.get_transition(curr_state, curr_command)
        if g.dev_mode:
            bot.send_message(chat_id=chat_id,
                             text=f'prev state: {curr_state.name} ({curr_state.value})\n'
                                  f'cmd: {curr_command.name} ({curr_command.value})\n'
                                  f'new state: {next_state.name} ({next_state.value})')

        # get state from service and render
        handler = state_service.states()[next_state]
        log.info(f'rendering state: {handler.__name__}')
        handler(bot, update, curr_context)

        # update params
        log.info(f'Updating state to: {next_state.name}')
        g.automata.set_state(chat.id, next_state)
        curr_context[CONTEXT_COMMANDS].append(curr_command)
        curr_context[CONTEXT_ACTION].append(curr_action)

        if g.dev_mode:
            print_dev_info(bot, chat_id, curr_context)

    except Exception as e:
        try:
            ERR_COUNTER[str(len(ERR_COUNTER.values()) + 1)] = {
                'datetime': str(datetime.datetime.now()),
                'chat': chat_id,
                'error': str(e),
                'context': str(curr_context)
            }
        except Exception:
            pass
        log.error('Error has been caught in handler: ', e)
        lang = curr_context[CONTEXT_LANG] if curr_context is not None else Language.ENG.value
        text = message_source[lang]['error']
        bot.send_message(chat_id=chat_id,
                         text=emojize(text, use_aliases=True),
                         parse_mode=ParseMode.MARKDOWN)

    else:
        log.info('<-- Successfully handled')


def reply_on_unknown(bot, chat_id):
    log.info('x-- Replying on unknown command')

    lang = g.automata.get_context(chat_id)[CONTEXT_LANG]
    text = message_source[lang]['filter.unknown']
    bot.send_message(chat_id=chat_id,
                     text=emojize(text, use_aliases=True),
                     parse_mode=ParseMode.MARKDOWN)


def print_dev_info(bot, chat_id, curr_context):
    context_commands = [c.name for c in curr_context[CONTEXT_COMMANDS]]
    context_task = curr_context[CONTEXT_TASK].get_id() if curr_context[CONTEXT_TASK] else '-'
    bot.send_message(chat_id=chat_id,
                     text=f'Latest task: {context_task}\nLatest commands: {context_commands}')
