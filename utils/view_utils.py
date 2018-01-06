"""
Created by anthony on 07.12.2017
view_utils
"""
import datetime

from components.message_source import message_source
from services import project_service

emoji_rocket = ':rocket: '
emoji_globe = ':earth_africa: '
emoji_upcoming = ':black_square_button: '
emoji_completed = ':white_check_mark: '
emoji_all = ':scroll: '
emoji_search = ':mag: '
emoji_mortal_reminder = ':alarm_clock: '


def render_task(task, lang):
    if task is None:
        raise AssertionError('Task is None')

    pretty_task = task.get_description()
    if not task.is_task_completed():
        pretty_task = '*' + task.get_description() + '*'

    project = project_service.find_project_by_id(task.get_project_id())
    category = message_source[lang][f'btn.new_task.project.{project.get_title()}.label']
    return pretty_task + ' (' + category + ') '


def render_task_with_timedelta(task, another_task, lang):
    if task is None:
        raise AssertionError('Task is None')
    if another_task is None:
        raise AssertionError('Task to be checked against is None')

    timedelta = None
    if task.get_next_remind_date() is not None \
            and another_task.get_next_remind_date() is not None:
        timedelta = task.get_next_remind_date() - another_task.get_next_remind_date()

    if timedelta < datetime.timedelta(0):
        timedelta = datetime.timedelta(hours=24) - timedelta

    pretty_print = render_task(another_task, lang)
    if timedelta:
        hours = timedelta.seconds // 3600
        if 1 == hours:
            pretty_print += message_source[lang]['date.hr'].format(hours) + '\n'

        elif 1 < hours:
            pretty_print += message_source[lang]['date.hrs'].format(hours) + '\n'

        else:
            minutes = timedelta.seconds // 60
            if 0 != minutes:
                pretty_print += message_source[lang]['date.min'].format(minutes) + '\n'

            else:
                pretty_print += message_source[lang]['date.same'] + '\n'

    return pretty_print


def concat_username(prefix, user, postfix):
    res = ''
    if user and 'none' != user.get_first_name().lower():
        res = prefix + user.get_first_name() + postfix

    else:
        res = prefix + postfix.capitalize()

    return res
