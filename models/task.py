"""
Created by anthony on 18.10.17
task
"""
from sqlalchemy import BigInteger, Column, String, DateTime, SmallInteger, ForeignKey, Boolean
from config.db_config import Base
import datetime
import logging

from models.abstract_entity import AbstractEntity
from services import notification_service as ns


log = logging.getLogger(__name__)


class Task(Base, AbstractEntity):
    __tablename__ = 'tasks'
    # task props
    id                  = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    description         = Column(String, nullable=False)
    is_completed        = Column(Boolean, default=False)
    priority            = Column(SmallInteger, default=1)
    create_date         = Column(DateTime, nullable=False)
    project_id          = Column(BigInteger, ForeignKey('projects.id'), nullable=False)
    # message props
    message_text        = Column(String)
    user_id             = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    # reminder props
    start_date          = Column(DateTime)
    end_date            = Column(DateTime)
    next_remind_date    = Column(DateTime)
    is_enabled          = Column(Boolean, default=True)
    is_periodic         = Column(Boolean, default=False)
    # safe delete flag
    is_active           = Column(Boolean, default=True)

    def __init__(self, description, user_id, project_id):
        super().__init__()
        self.set_description(description.capitalize())
        self.set_user_id(user_id)
        self.set_project_id(project_id)
        # do not need it now
        self.set_priority(1)
        # original message
        self.set_message_text(description)
        self.notification_job = None
        self.next_remind_date = None
        # explicitly setting current datetime from python since postgres writes in UTC by default
        self.create_date = datetime.datetime.now()
        self.start_date = datetime.datetime.now()

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def set_description(self, descr):
        if not descr:
            raise ValueError('Task description text cannot be empty')
        self.description = descr

    def get_create_date(self):
        return self.create_date

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_project_id(self):
        return self.project_id

    def set_project_id(self, proj_id):
        self.project_id = proj_id

    def get_priority(self):
        return self.priority

    def set_priority(self, prior):
        self.priority = prior

    def increase_priority(self, value=1):
        self.priority += value

    def decrease_priority(self, value=1):
        self.priority -= value

    def set_message_text(self, msg_text):
        if not msg_text:
            raise ValueError('Message text cannot be empty')
        self.message_text = msg_text

    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_end_date(self, end_date):
        if end_date < datetime.datetime.now():
            raise ValueError('End date cannot be in past')
        self.end_date = end_date

    def get_next_remind_date(self):
        return self.next_remind_date

    def set_next_remind_date(self, next_remind_date):
        if next_remind_date < datetime.datetime.now():
            raise ValueError('Next remind date cannot be in past')

        self.next_remind_date = next_remind_date

        log.info(f'Creating notification for task {self.id}')
        notification = ns.create_notification(self.get_user_id(), self)

        if notification is None:
            log.error(f'Notification is none for task id {self.id}')

        self.notification_job = notification
        self.mark_as_enabled()


    def mark_as_periodic(self):
        self.is_periodic = True

    def mark_as_completed(self):
        self.is_completed = True

    def mark_as_not_completed(self):
        self.is_completed = False

    def is_task_completed(self):
        return self.is_completed

    def mark_as_disabled(self):
        self.is_enabled = False

    def mark_as_enabled(self):
        self.is_enabled = True

    def is_task_enabled(self):
        return self.is_enabled
