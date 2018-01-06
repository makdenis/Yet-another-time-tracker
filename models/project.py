"""
Created by anthony on 19.10.17
project
"""
from enum import Enum

from sqlalchemy import BigInteger, Column, String, ForeignKey, Boolean
from config.db_config import Base

from models.abstract_entity import AbstractEntity


class ProjectType(Enum):
    OTHER = 'oth'
    PERSONAL = 'prs'
    STUDY = 'std'
    WORK = 'wrk'


class Project(Base, AbstractEntity):
    __tablename__ = 'projects'
    id                  = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    # category e.g. personal / university / work
    title               = Column(String)
    # closest task by next_remind_date
    next_task_id        = Column(BigInteger, ForeignKey('tasks.id'), nullable=True)
    user_id             = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    # safe delete flag
    is_active           = Column(Boolean, default=True)

    def __init__(self, user_id, title):
        super().__init__()
        self.set_title(ProjectType.OTHER.value if title is None else title)
        self.set_user_id(user_id)

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def set_title(self, title):
        if not title:
            raise ValueError('Project title cannot be empty')
        self.title = title

    def get_next_task_id(self):
        return self.next_task_id

    def set_next_task_id(self, nxt_task_id):
        self.next_task_id = nxt_task_id

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id
