"""
Created by anthony on 23.10.17
user_service.py
"""
import logging

from models.user import User
from utils.db_utils import save, flush, find_all, find_one_by_id


log = logging.getLogger(__name__)


def find_user_by_username(username):
    users = find_all(User)
    for u in users:
        if username == u.get_username():
            return u
    return None


def find_user_by_id(user_id):
    return find_one_by_id(user_id, User)


def create_or_get_user(chat):
    chat_id = int(chat.id)
    log.info(f'Checking if user with id {chat_id} exists')

    user_by_id = find_one_by_id(chat_id, User)
    if user_by_id:
        log.debug(f'User with id {chat_id} already exists')
        return user_by_id

    else:
        log.info('User not found. Creating new one')
        username = chat.username
        first_name = chat.first_name

        log.debug('Flushing session')
        user = flush(User(username=username, chat_id=chat_id, first_name=first_name))

        log.debug('Saving user')
        saved_user = save(user)
        return saved_user


def update_user(user):
    saved_user = save(user)
    return saved_user
