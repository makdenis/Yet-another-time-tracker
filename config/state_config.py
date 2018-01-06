"""
Created by anthony on 12.11.17
automata_config
"""
from enum import Enum


TRANSITION_TABLE = [
    # start echo    task    date    all     lang
    [0,     2,      3,      0,      1,      6],     # 0. start
    [0,     2,      3,      5,      1,      6],     # 1. all tasks
    [0,     2,      3,      4,      1,      6],     # 2. new task
    [0,     2,      3,      4,      1,      6],     # 3. view task
    [0,     2,      3,      4,      1,      4],     # 4. edit date
    [0,     2,      3,      5,      1,      6],     # 5. error
    [0,     1,      5,      5,      1,      0],     # 6. select language
]


class State(Enum):
    """
    Each value defines row(state) in Transition table
    """
    START = 0
    ALL_TASKS = 1
    NEW_TASK = 2
    VIEW_TASK = 3
    EDIT_DATE = 4
    ERROR = 5
    SELECT_LANG = 6


class CommandType(Enum):
    """
    Each value defines column(signal) in Transition table
    """
    UNKNOWN = -1
    START = 0
    ECHO = 1
    VIEW = 2
    DATE = 3
    ALL = 4
    LANG = 5


class Language(Enum):
    ENG = 'eng'
    RUS = 'rus'


# Defines aliases for each command (signal (column in table))
CommandAliases = {
    CommandType.START: ['/start', '/hi', '/привет', '/дратути'],
    CommandType.ALL: ['/all', '/все', '/задачи'],
    CommandType.VIEW: ['/id', '/task', '/задача', '/таск'],
    CommandType.DATE: ['/date', '/дата'],
    CommandType.LANG: ['/lang', '/language', '/язык'],
    # CommandType.ECHO: ['']
}


class Action(Enum):
    """
    README!
    As short as possible string that is passed with button callback
    since there is a length limit per callback date (only 64 bytes!)
    """
    TASK_VIEW = 'view'
    TASK_MARK_AS_DONE = 'mark_done'
    TASK_DELETE = 'del'
    TASK_DISABLE = 'disable'
    TASK_PROJECT_SELECTED = 'task_proj'
    LIST_UPCOMING = 'upcoming'
    LIST_COMPLETED = 'done'
    LIST_ALL = 'all'
    VIEW_LANG = 'all_langs'
    SELECTED_LANG = 'sel_lang'
    START = 'home'


# These are keys for fields in callback data passed on button callback
# These strings are also counted as payload in data
# and so should be as short as possible
class CallbackData(Enum):
    """
    ACTION: Actions describe the fact that something happened,
        but don't specify how the application's state changes in response.
        (c) React Redux
    DATA: Payload that is used for rendering state
        e.g.: task_id, or flag that should define what to render - all_tasks
        or just completed ones.
    COMMAND: Analogue of regular command that should define which state to render

    In other words:
        COMMAND: which state to render?
        ACTION: how to render?
        DATA: which data to insert into state?
    """
    ACTION = 'act'
    DATA = 'dt'
    COMMAND = 'cmd'


ADMINS = [
    316956601
]
