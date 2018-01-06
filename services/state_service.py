"""
Created by anthony on 12.11.17
state_service
"""
import datetime
import logging

from emoji import emojize
from telegram import ParseMode

import components.keyboard_builder as kb
import g
from components.automata import CONTEXT_TASK, CONTEXT_COMMANDS, CONTEXT_LANG
from components.message_source import message_source
from config.state_config import State, Language, CallbackData, Action
from services import user_service, task_service, project_service
from utils import view_utils, date_utils
from utils.date_utils import readable_datetime
from utils.handler_utils import is_callback, deserialize_data
from utils.view_utils import concat_username, emoji_rocket, emoji_globe, emoji_upcoming, emoji_completed, emoji_all, \
    emoji_search


log = logging.getLogger(__name__)


def states():
    return {
        State.START: start_state,
        State.ALL_TASKS: all_tasks_state,
        State.SELECT_LANG: select_lang_state,
        State.NEW_TASK: new_task_state,
        State.VIEW_TASK: view_task_state,
        State.EDIT_DATE: edit_date_state,
        State.ERROR: error_state,
    }


def start_state(bot, update, context):
    chat = update.effective_chat
    chat_id = chat.id
    user = user_service.create_or_get_user(chat)

    if is_callback(update):
        deserialized = deserialize_data(update.callback_query.data)
        action = deserialized[CallbackData.ACTION]

        if action is Action.SELECTED_LANG:
            lang = deserialized[CallbackData.DATA]
            context[CONTEXT_LANG] = Language(lang)

    lang = context[CONTEXT_LANG]
    welcome_text = concat_username(emoji_rocket + '*', user, ', ' + message_source[lang]['state.start_state.welcome'])

    num_all, num_upcoming, num_completed = task_service.find_stats_for_user(chat_id)
    bot_ver = 19  # because why not? :)
    completed_percent = 0 if 0 == num_all else int(num_completed / num_all * 100)
    num_completed = f'{num_completed} ({completed_percent} %)'
    num_upcoming = f'{num_upcoming} ({0 if 0 == num_all else (100 - completed_percent)} %)'
    welcome_text = welcome_text.format(num_upcoming, num_completed, num_all, bot_ver)

    bot.send_message(chat_id=chat_id,
                     text=emojize(welcome_text, use_aliases=True),
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=kb.StartStateKb(lang).build())


# TODO add refresh list button. if task was deleted it still remains in a list. add re-render list button
def all_tasks_state(bot, update, context):
    chat = update.effective_chat
    chat_id = chat.id
    lang = context[CONTEXT_LANG]
    user = user_service.create_or_get_user(chat)
    user_id = chat_id

    action = None
    if is_callback(update):
        deserialized = deserialize_data(update.callback_query.data)
        action = deserialized[CallbackData.ACTION]

    tasks = []
    text = None
    if not is_callback(update) or action is Action.LIST_ALL:
        tasks = task_service.find_tasks_by_user_id(user_id)
        text = concat_username(emoji_all + '*', user, ', ' + message_source[lang]['state.all_tasks.tasks.all'])

    elif action is Action.LIST_UPCOMING:
        tasks = task_service.find_upcoming_tasks_by_user_id(user_id)
        text = concat_username(emoji_upcoming + '*', user, ', ' + message_source[lang]['state.all_tasks.tasks.upcoming'])

    elif action is Action.LIST_COMPLETED:
        tasks = task_service.find_completed_tasks_by_user_id(user_id)
        text = concat_username(emoji_completed + '*', user, ', ' + message_source[lang]['state.all_tasks.tasks.completed'])

    if 0 == len(tasks):
        text_no_tasks = message_source[lang]['state.all_tasks.no_tasks_yet']
        notes = message_source[lang]['state.all_tasks.notes.no_tasks_yet']
        text = concat_username(emoji_search + '*', user, ', ' + text_no_tasks + notes)

    else:
        text += message_source[lang]['state.all_tasks.notes']

    tasks = sorted(tasks, key=lambda t: t.get_create_date())
    bot.send_message(chat_id=chat_id,
                     text=emojize(text, use_aliases=True),
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=kb.TasksAsButtons(tasks, lang).build())


def select_lang_state(bot, update, context):
    chat = update.effective_chat
    chat_id = chat.id

    user = user_service.create_or_get_user(chat)

    action = None
    if is_callback(update):
        deserialized = deserialize_data(update.callback_query.data)
        action = deserialized[CallbackData.ACTION]

    # find out what are we doing now? selecting lang or just showing available langs
    text = None
    if action is Action.SELECTED_LANG:
        deserialized = deserialize_data(update.callback_query.data)
        lang_string = deserialized[CallbackData.DATA]
        lang = Language(lang_string)
        context[CONTEXT_LANG] = lang

        text = message_source[lang]['btn.select_lang.' + lang_string + '.result']
        buttons = kb.StartStateKb(lang).build()

    elif action is Action.VIEW_LANG:
        # It's callback. nevertheless just show available langs
        lang = context[CONTEXT_LANG]
        text = concat_username(emoji_globe + '*', user, ', ' + message_source[lang]['state.select_lang'])
        buttons = kb.SelectLangKb(lang).build()

    else:
        # It's not callback. just show available langs
        lang = context[CONTEXT_LANG]
        text = concat_username(emoji_globe + '*', user, ', ' + message_source[lang]['state.select_lang'])
        buttons = kb.SelectLangKb(lang).build()

    bot.send_message(chat_id=chat_id,
                     text=emojize(text, use_aliases=True),
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=buttons)


def new_task_state(bot, update, context):
    chat = update.effective_chat
    chat_id = chat.id
    lang = context[CONTEXT_LANG]

    new_task = task_service.create_task(update)

    if g.test_mode:
        log.debug(f'Automatically setting reminder time for task {new_task.get_id()}')
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now() + datetime.timedelta(days=1)
        parsed_datetime = date_utils.random_date(d1, d2)

        new_task.set_next_remind_date(parsed_datetime)
        task_service.update_task(new_task)

    text = None
    markup = None
    if new_task:
        context[CONTEXT_TASK] = new_task

        text, markup = view_task_template_and_markup(lang, new_task, State.NEW_TASK)
        markup = kb.SelectProjectKb(lang).build()
    else:
        text = message_source[lang]['state.new_task.not_created']

    bot.send_message(chat_id=chat_id,
                     text=emojize(text, use_aliases=True),
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=markup)


def view_task_state(bot, update, context):
    chat = update.effective_chat
    chat_id = chat.id
    lang = context[CONTEXT_LANG]

    task_id = None
    action = None
    if is_callback(update):
        deserialized = deserialize_data(update.callback_query.data)
        task_id = deserialized[CallbackData.DATA]
        action = deserialized[CallbackData.ACTION]

        if action is Action.TASK_PROJECT_SELECTED:
            task = context[CONTEXT_TASK]
            # if bot was restarted then it has not tasks in context. then get latest task
            if task is None:
                task = task_service.find_latest_task_by_user_id(chat_id)

            task_id = task.get_id()

    else:
        args = update.message.text.split()
        task_id = args[1]

    user = user_service.create_or_get_user(chat)
    task = task_service.find_task_by_id_and_user_id(task_id, user.get_id())

    # if task was removed do not show anything
    if task and task.is_flag_active():
        reply_text, reply_markup = view_task_template_and_markup(lang, task, State.VIEW_TASK)

        if action is Action.TASK_MARK_AS_DONE:
            reply_markup = None
            if task.is_task_completed():
                task.mark_as_not_completed()
                reply_text = message_source[lang]['btn.view_task.mark_undone.result']

            else:
                task.mark_as_completed()
                reply_text = message_source[lang]['btn.view_task.mark_as_done.result']

            text_on_edit, markup_on_edit = view_task_template_and_markup(lang, task, State.VIEW_TASK)
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=update.effective_message.message_id,
                                  text=emojize(text_on_edit, use_aliases=True),
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=markup_on_edit)

        elif action is Action.TASK_DISABLE:
            reply_markup = None
            if task.is_task_enabled():
                task.mark_as_disabled()
                reply_text = message_source[lang]['btn.view_task.disable_notify.result'].format(task.get_description())

            else:
                task.mark_as_enabled()
                reply_text = message_source[lang]['btn.view_task.enable_notify.result'].format(task.get_description())

            text_on_edit, markup_on_edit = view_task_template_and_markup(lang, task, State.VIEW_TASK)
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=update.effective_message.message_id,
                                  text=emojize(text_on_edit, use_aliases=True),
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=markup_on_edit)


        elif action is Action.TASK_DELETE:
            task.mark_as_inactive()
            reply_text = message_source[lang]['btn.view_task.delete_task.result'].format(task.get_id())
            reply_markup = None

            bot.delete_message(chat_id=chat_id,
                               message_id=update.callback_query.message.message_id)

        elif action is Action.TASK_VIEW:
            # It's not callback, then just render the state
            reply_text, reply_markup = view_task_template_and_markup(lang, task, State.VIEW_TASK)

        # set project id by editing current TASK_VIEW
        elif action is Action.TASK_PROJECT_SELECTED:
            deserialized = deserialize_data(update.callback_query.data)
            project_value = deserialized[CallbackData.DATA]

            project_selected = project_service.create_or_get_project(user.get_id(), project_value)
            task.set_project_id(project_selected.get_id())
            task_service.update_task(task)

            context[CONTEXT_TASK] = task

            text_on_edit, markup_on_edit = view_task_template_and_markup(lang, task, State.VIEW_TASK)
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  text=emojize(text_on_edit, use_aliases=True),
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=markup_on_edit)
            return

        # update task
        task_service.update_task(task)

        # set updated task to context
        context[CONTEXT_TASK] = task

        bot.send_message(chat_id=chat_id,
                         text=emojize(reply_text, use_aliases=True),
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=reply_markup)

    else:
        task_inactive = message_source[lang]['state.view_task.inactive']
        bot.send_message(chat_id=chat_id,
                         text=emojize(task_inactive, use_aliases=True))


def edit_date_state(bot, update, context):
    chat = update.effective_chat
    chat_id = chat.id
    lang = context[CONTEXT_LANG]
    latest_task = context[CONTEXT_TASK]

    err_cause = None
    if latest_task and latest_task.is_flag_active():

        args = update.message.text.split()
        datetime_args = args[1:]
        parsed_datetime = None
        if g.dev_mode or g.test_mode:
            seconds = int(datetime_args[0]) or 10
            parsed_datetime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

        else:
            try:
                parsed_datetime = date_utils.parse_date_msg(datetime_args)

            except Exception as e:
                log.error('Could not parse datetime: ', e)
                task_inactive = message_source[lang]['state.edit_date.parse_error']
                bot.send_message(chat_id=chat_id,
                                 text=emojize(task_inactive, use_aliases=True),
                                 parse_mode=ParseMode.MARKDOWN)

        latest_task.set_next_remind_date(parsed_datetime)
        task_service.update_task(latest_task)

        reply_text = message_source[lang]['state.edit_date.success'].format(readable_datetime(parsed_datetime))

        # find if reminder intersects with another tasks
        nearest_tasks = list(set(task_service.find_tasks_within_timedelta(latest_task, datetime.timedelta(hours=8))))
        if 0 != len(nearest_tasks):
            render_num = min([3, len(nearest_tasks)])
            tasks_to_show = ''
            for t in nearest_tasks[0:render_num]:
                tasks_to_show += view_utils.render_task_with_timedelta(latest_task, t, lang)

            reply_text += message_source[lang]['state.edit_date.intersect'].format(tasks_to_show)
            reply_text += message_source[lang]['state.edit_date.intersect.notes']

        bot.send_message(chat_id=chat_id,
                         text=emojize(reply_text, use_aliases=True),
                         parse_mode=ParseMode.MARKDOWN)

    else:
        task_inactive = message_source[lang]['state.view_task.inactive']
        bot.send_message(chat_id=chat_id,
                         text=emojize(task_inactive, use_aliases=True),
                         parse_mode=ParseMode.MARKDOWN)


def error_state(bot, update, context):
    chat = update.effective_chat
    chat_id = chat.id

    lang = context[CONTEXT_LANG]
    latest_task = context[CONTEXT_TASK]

    if latest_task:
        command_trace = [c.name for c in context[CONTEXT_COMMANDS]]
        bot.send_message(chat_id=chat_id,
                         text=emojize(message_source[lang]['error'].format(latest_task.get_id(), command_trace)),
                         use_aliases=True,
                         parse_mode=ParseMode.MARKDOWN)

    else:
        log.warning("No task in context found")


def view_task_template_and_markup(lang, task, state):
    if not (state is State.NEW_TASK or state is State.VIEW_TASK):
        raise ValueError('Task template cannot be filled for state: ' + state._name_)

    new_or_review_title = message_source[lang][
        'state.new_task.created' if state is State.NEW_TASK else 'state.view_task.review'
    ]

    project = project_service.find_project_by_id(task.get_project_id())
    project_to_show = message_source[lang]['btn.new_task.project.' + project.get_title() + '.label']
    if state is State.NEW_TASK:
        project_to_show = message_source[lang]['project.not_selected']

    status_to_show = message_source[lang]['task.completed' if task.is_task_completed() else 'task.upcoming']

    # show remind date like this: '21 dec 13:37' or like this if muted: '21 dec 13:37 (Muted)'
    reminder_to_show = readable_datetime(task.get_next_remind_date()) + ' ' + \
                       (message_source[lang]['task.muted'] if not task.is_task_enabled() else '')

    template = message_source[lang]['state.view_task']
    filled_template = template.format(new_or_review_title,
                                      task.get_description(),
                                      reminder_to_show,
                                      readable_datetime(task.get_create_date()),
                                      project_to_show,
                                      status_to_show,
                                      task.get_id())

    markup = kb.ViewTaskKb(task.get_id(), lang)

    if not task.is_task_enabled():
        unmute_button = kb.ViewTaskCommandButton('btn.view_task.enable_notify.label', lang, Action.TASK_DISABLE, data=task.get_id())
        markup.set_button_at_position(unmute_button, 0, 1)

    if task.is_task_completed():
        undone_button = kb.ViewTaskCommandButton('btn.view_task.mark_undone.label', lang, Action.TASK_MARK_AS_DONE, data=task.get_id())
        markup.set_button_at_position(undone_button, 0, 0)

    built_markup = markup.build()
    return filled_template, built_markup
