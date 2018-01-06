"""
Created by anthony on 23.10.17
project_service
"""
import logging

from models.project import Project, ProjectType
from services import task_service
from utils.db_utils import save, flush, find_all, find_one_by_id


log = logging.getLogger(__name__)


def find_projects_by_user_id(user_id_value):
    user_id = int(user_id_value)
    projects = find_all(Project)
    projects_by_user = [p for p in projects if user_id == p.get_user_id()]
    return projects_by_user


def find_project_by_id(project_id_value):
    project_id = int(project_id_value)
    return find_one_by_id(project_id, Project)


def create_or_get_project(user_id_value, project_type_value):
    # validate at first
    user_id = int(user_id_value)
    project = ProjectType(project_type_value)

    projects_of_user = find_projects_by_user_id(user_id)
    # check if there is already a project with same title(category)
    for p in projects_of_user:
        if p.get_title() == project.value:
            return p

    # there is no such project -> create new one
    flushed_proj = flush(Project(user_id, project.value))
    saved_proj = save(flushed_proj)
    return saved_proj


def update_project(project):
    saved = save(project)
    return saved


def update_nearest_task_for_user_project(project_id_value, user_id_value):
    log.info(f'Updating nearest task for project ({project_id_value}) and user {user_id_value}')
    # try cast to int to prevent getting project here. we need only it's id here
    user_id = int(user_id_value)
    project_id = int(project_id_value)
    project = find_one_by_id(project_id, Project)

    if project:

        user_tasks = task_service.find_tasks_by_user_id(user_id)
        tasks_by_project_id = [t for t in user_tasks
                               if t.get_project_id() == project_id and t.get_next_remind_date() is not None]
        sorted_by_next_remind_date = sorted(tasks_by_project_id, key=lambda t: t.get_next_remind_date())

        if 0 != len(sorted_by_next_remind_date):
            nearest_task = sorted_by_next_remind_date[0]
            project.set_next_task_id(nearest_task)

            saved_proj = save(project)
            return saved_proj

        else:
            log.info(f'task list is empty')
            return project

    else:
        log.error(f'No projects found by project id {project_id_value} for user {user_id_value}')
