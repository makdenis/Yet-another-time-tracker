"""
Created by anthony on 22.10.17
task_service

if you are not sure which service should implement function
then implement it in it's return type service
e.g. get all user's tasks: return type is Task -> task_service.find_all_by_user_id
"""
import logging

from models.project import ProjectType
from models.task import Task
from services import project_service, user_service
from utils import date_utils
from utils.db_utils import flush, save, find_all, find_one_by_id, find_active_and_inactive


log = logging.getLogger(__name__)


def find_all_tasks():
    return find_all(Task)


def find_tasks_by_description(title):
    all_tasks = find_all(Task)
    res = [t for t in all_tasks if title in t.get_description()]
    return res


def find_task_by_id_and_user_id(task_id_value, user_id):
    """
    returns selected task only if it was made by user provided
    otherwise throws permission exception
    """
    task_id = int(task_id_value)
    task_by_id = find_one_by_id(task_id, Task)

    if task_by_id and task_by_id.get_user_id() == user_id:
        return task_by_id

    else:
        raise PermissionError(f'User with id {user_id} is not permitted '
                              f'to access task with id {task_id}')


def find_tasks_by_user_id(user_id_value):
    user_id = int(user_id_value)
    all_tasks = find_all(Task)
    tasks_by_user = [t for t in all_tasks if user_id == t.get_user_id()]
    return tasks_by_user


def find_upcoming_tasks_by_user_id(user_id_value):
    user_id = int(user_id_value)
    tasks = find_tasks_by_user_id(user_id)
    upcoming = [t for t in tasks if t.is_task_completed() is False]
    return upcoming


def find_completed_tasks_by_user_id(user_id_value):
    user_id = int(user_id_value)
    tasks = find_tasks_by_user_id(user_id)
    upcoming = [t for t in tasks if t.is_task_completed() is True]
    return upcoming


def find_nearest_task(user_id_value, project_id_value):
    user_id = int(user_id_value)
    project_id = int(project_id_value)

    all_tasks = find_all(Task)
    tasks_by_user_id = filter(
        lambda t: t.get_user_id() == user_id and t.get_project_id() == project_id, all_tasks)

    sorted_by_remind_date = sorted(
        tasks_by_user_id, key=lambda t: t.get_next_remind_date())

    return sorted_by_remind_date[0]


def create_task(update):
    # create or get user
    chat = update.message.chat
    user = user_service.create_or_get_user(chat)

    # create or get project
    basic_type = ProjectType.OTHER.value
    project = project_service.create_or_get_project(user.get_id(), basic_type)

    if project and user:
        log.info(f'Creating task for user {user.get_id()}')

        msg_text = update.message.text
        new_task = Task(description=msg_text, user_id=user.get_id(), project_id=project.get_id())
        flushed_task = flush(new_task)
        saved_task = save(flushed_task)
        return saved_task

    else:
        raise ValueError('Project or User could not be created. So does Task')


def update_task(task):
    saved_task = save(task)
    return saved_task


def find_tasks_within_timedelta(task_to_check, time_delta_threshold):
    log.debug(f'checking if task is within threshold: {time_delta_threshold}')

    user_id = task_to_check.get_user_id()
    tasks = find_tasks_by_user_id(user_id)
    tasks_with_reminder = [t for t in tasks if t.get_next_remind_date() is not None
                           and t.is_task_completed() is False
                           and t.get_id() != task_to_check.get_id()]

    nearest_tasks = []
    for task in tasks_with_reminder:
        time_delta = task.get_next_remind_date() - task_to_check.get_next_remind_date()

        if abs(time_delta.total_seconds()) < time_delta_threshold.total_seconds():
            nearest_tasks.append(task)

    nearest_tasks_sorted = sorted(nearest_tasks,
                                  key=lambda t: abs(date_utils.seconds_between_tasks(t, task_to_check)))
    return nearest_tasks_sorted


def find_stats_for_user(user_id_val):
    user_id = int(user_id_val)
    all_by_user = len(find_tasks_by_user_id(user_id))
    upcoming = len(find_upcoming_tasks_by_user_id(user_id))
    completed = len(find_completed_tasks_by_user_id(user_id))
    return all_by_user, upcoming, completed


def find_latest_task_by_user_id(user_id_value):
    user_id = int(user_id_value)
    tasks = find_tasks_by_user_id(user_id)
    tasks = sorted(tasks, key=lambda t: t.get_create_date(), reverse=True)
    return tasks[0]
