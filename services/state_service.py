"""
Created by anthony on 12.11.17
state_service
"""
from components.automata import CONTEXT_TASK, CONTEXT_COMMANDS
from services import user_service, task_service
from config.state_config import State
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils import handler_utils
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


def states():
    return {
        State.START: start_state,
        State.ALL_TASKS: all_tasks_state,
        State.NEW_TASK: new_task_state,
        State.VIEW_TASK: view_task_state,
        State.EDIT_DATE: edit_date_state,
        State.ERROR: error_state
    }


def start_state(bot, update, context):
    chat = update.message.chat
    user = user_service.create_or_get_user(chat)

    reply_msg = 'Hello'
    if user:
        reply_msg += ', ' + user.get_first_name()

    update.message.reply_text(reply_msg)


def all_tasks_state(bot, update, context):
    chat = update.message.chat
    user = user_service.create_or_get_user(chat)
    user_tasks = task_service.find_tasks_by_user_id(user.get_id())

    tasks_to_show = [f'[{t.get_id()}] {t.get_description()}' for t in user_tasks]

    first_name = user.get_first_name()
    if 0 == len(tasks_to_show):
        update.message.reply_text(f'{first_name}, you don\'t have any tasks yet')
        update.message.reply_text('Just write me something to create a new one :)')

    else:
        keyboard = []
        id = 1
        for task in tasks_to_show:
            keyboard.append([InlineKeyboardButton(str(task), callback_data=str(id))])
            id = id + 1
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(first_name + ', here are your tasks:\n', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    task_id = query.data
    chat = query.message.chat
    user = user_service.create_or_get_user(chat)
    task = task_service.find_task_by_id_and_user_id(task_id, user.get_id())
    #context[CONTEXT_TASK] = task
    task_descr = task.get_description()
    bot.edit_message_text(text=f'[{task_id}]: {task_descr}',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def new_task_state(bot, update, context):
    chat = update.message.chat
    new_task = task_service.create_task(update)

    if new_task:
        context[CONTEXT_TASK] = new_task

        reply_on_success = f'task with id "{new_task.get_id()}" has been created!'
        user = user_service.create_or_get_user(chat)
        if user:
            reply_on_success = user.get_first_name() + ', ' + reply_on_success

        update.message.reply_text(reply_on_success.capitalize())


def view_task_state(bot, update, context):
    args = update.message.text.split()
    task_id = args[1]

    chat = update.message.chat
    user = user_service.create_or_get_user(chat)

    task = task_service.find_task_by_id_and_user_id(task_id, user.get_id())
    if task:
        context[CONTEXT_TASK] = task

        task_descr = task.get_description()
        update.message.reply_text(f'[{task_id}]: {task_descr}')

    else:
        first_name = user.get_first_name()
        update.message.reply_text(f'Sorry, {first_name}, I couldn\'t find task with id "{task_id}"')


def edit_date_state(bot, update, context):
    args = update.message.text.split()
    datetime_args = args[1:]
    latest_task = context[CONTEXT_TASK]

    if latest_task:
        user_id = update.message.chat.id
        latest_task_by_user = task_service.find_task_by_id_and_user_id(latest_task.get_id(), user_id)

        if latest_task_by_user:
            parsed_datetime = handler_utils.parse_date_msg(datetime_args)
            latest_task_by_user.set_next_remind_date(parsed_datetime)

            update.message.reply_text(f'Setting date to {parsed_datetime} for task:')
            update.message.reply_text(f'[{latest_task.get_id()}]: {latest_task.get_description()}')
            return

    update.message.reply_text(f'Sorry, I could not find that task')


def error_state(bot, update, context):
    lastest_task_id = context[CONTEXT_TASK].get_id()
    command_trace = [c.name for c in context[CONTEXT_COMMANDS]]

    update.message.reply_text(f'Error. Latest task id: {lastest_task_id}. Command trace: {command_trace}')
