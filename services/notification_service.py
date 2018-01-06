"""
Created by anthony on 17.11.17
notification_service
"""
import logging
from emoji import emojize
import datetime

from telegram import ParseMode

import g
from components.automata import CONTEXT_LANG
import components.keyboard_builder as kb
from components.message_source import message_source
from services import task_service, user_service
from utils.date_utils import readable_datetime
from utils.view_utils import concat_username, emoji_mortal_reminder

log = logging.getLogger(__name__)


PAYLOAD_CHAT_ID = 'payload_chat_id'
PAYLOAD_TASK_ID = 'payload_task_id'


# TODO create_or_get or another way to remove previous notification when a new one has been set
def create_notification(chat_id, task):
    payload = {
        PAYLOAD_CHAT_ID: chat_id,
        PAYLOAD_TASK_ID: task.get_id()
    }
    remind_date = task.get_next_remind_date()
    log.info(f'Creating notification for chat ({chat_id}) on time ({remind_date})')
    job = g.queue.run_once(callback=notification_callback, when=remind_date, context=payload)
    return job


def notification_callback(bot, job):
    payload = job.context  # passed here via run_once(.. context=...)

    if payload:
        # chat id can be not int. e.g. '@username' is chat_id too
        chat_id, task_id = map(payload.get, (PAYLOAD_CHAT_ID, PAYLOAD_TASK_ID))
        chat_id = int(chat_id)

        task = task_service.find_task_by_id_and_user_id(task_id, chat_id)
        if task.is_task_enabled() is False or task.is_task_completed():
            log.info(f'Notification for task {task_id} in chat ({chat_id}) is disabled. Skipping')
            return

        lang = g.automata.get_context(chat_id)[CONTEXT_LANG]

        user = user_service.find_user_by_id(chat_id)

        reminder = message_source[lang]['state.edit_date.reminder'].format(
            task.get_description(), readable_datetime(task.get_create_date()))
        reply_text = concat_username(emoji_mortal_reminder + '*', user, ', ' + reminder)

        markup = kb.ViewTaskKb(task_id, lang).build()

        bot.send_message(chat_id=chat_id,
                         text=emojize(reply_text, use_aliases=True),
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)

    else:
        log.error('No payload found in notification callback')


def load_tasks_to_queue():
    """
    Gets all tasks that will be fired in future and sets them to job queue
    This method is originally made to not forget notifications in queue when bot is restarted
    """
    all_tasks = task_service.find_all_tasks()
    now = datetime.datetime.now()
    tasks_not_yet_fired = [t for t in all_tasks if t.get_next_remind_date() is not None
                           and now < t.get_next_remind_date()]

    log.info(f'Creating notifications for {len(tasks_not_yet_fired)} tasks')
    for t in tasks_not_yet_fired:
        create_notification(t.get_user_id(), t)


    return tasks_not_yet_fired
