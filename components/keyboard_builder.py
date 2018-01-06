"""
Created by anthony on 09.12.2017
keyboard_builder
"""
import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from abc import ABC, abstractmethod

from components.message_source import message_source
from config.state_config import Action, CallbackData, Language, CommandType
from models.project import ProjectType


log = logging.getLogger(__name__)


BTN_LABEL = 'button_label'
BTN_DATA = 'button_data'
BTN_COMMAND = 'button_command_analogue'
# Actions describe the fact that something happened, but don't specify how the app's state changes in response.
# This is the job of reducers. (c) React Redux
BTN_ACTION = 'button_action'

DATA_LIMIT_IN_BYTES = 64


class Button:
    def __init__(self, label, lang, action, command, data=None):
        if type(action) is not Action:
            raise ValueError('Action provided to button is not of Action type: ' + action)

        if type(command) is not CommandType:
            raise ValueError('Command provided to button is not of Command type: ' + command)

        self.label = str(label) if lang is None else message_source[lang][label]  # in case of task as button
        self.data = str(data) if data is not None else 'sao'
        self.action = action.value
        self.command = command.value

    def set_label(self, new_label):
        self.label = new_label

    def set_data(self, new_data):
        if new_data is None or '' == new_data:
            raise ValueError('Explicitly defined data cannot be empty or null')

        self.data = new_data

    def build(self):
        # this data is passed to callback and is accepted by action reducer
        data = {
            CallbackData.ACTION.value: self.action,
            CallbackData.DATA.value: self.data,
            CallbackData.COMMAND.value: self.command
        }
        serialized_data = json.dumps(data)

        encoded = serialized_data.encode('utf-8')
        if len(encoded) > DATA_LIMIT_IN_BYTES:
            raise ValueError(f'Too large data is going to be passed to to callback: '
                             f'{len(encoded)} bytes. Limit: {DATA_LIMIT_IN_BYTES} bytes')

        new_button = InlineKeyboardButton(emojize(self.label, use_aliases=True), callback_data=serialized_data)
        return new_button


class ViewTaskCommandButton(Button):
    def __init__(self, label, lang, action, data):
        super().__init__(label, lang, action, CommandType.VIEW, data)


class StartCommandButton(Button):
    def __init__(self, label, lang):
        super().__init__(label, lang, Action.START, CommandType.START)


class AllTasksCommandButton(Button):
    def __init__(self, label, lang, action):
        super().__init__(label, lang, action, CommandType.ALL)


class ViewLangCommandButton(Button):
    def __init__(self, label, lang, action):
        super().__init__(label, lang, action, CommandType.LANG)


class SelectLangButton(ViewLangCommandButton):
    """
    Command type and action are already set up
    """
    def __init__(self, label, lang, lang_data):
        super().__init__(label, lang, Action.SELECTED_LANG)
        self.set_data(lang_data.value)


class SelectProjectButton(ViewTaskCommandButton):
    """
    Command type, data and action are already set up
    """
    def __init__(self, lang, project):
        def build_title(str):
            return f'btn.new_task.project.{str}.label'

        super().__init__(build_title(project.value), lang, Action.TASK_PROJECT_SELECTED, data=project.value)



class Keyboard(ABC):
    def __init__(self, button_grid):
        self.button_grid = button_grid

    def set_button_grid(self, new_button_grid):
        self.button_grid = new_button_grid

    def set_button_at_position(self, new_button, row, col=None):
        if list == type(self.button_grid[row]):
            if col is None or col >= len(self.button_grid[row]):
                raise ValueError('Column is null or out of range')

            self.button_grid[row][col] = new_button

        else:
            self.button_grid[row] = new_button

    def build(self):
        """
                Creates _inline_ keyboard and returns it's markup with grid of buttons like this:
                [
                    { English },
                    { Русский }
                ],
                { Exit },
                [
                    { X },
                    { AB },
                    { Y }
                ]

                -->

                [ English ][ Русский ]
                [        Exit        ]
                [  X  ][  AB  ][  Y  ]
                """
        def is_singleton_list(obj):
            return list == type(obj) and 1 == len(obj)

        if self.button_grid is None:
            raise ValueError('Button grid is empty. Cannot build keyboard')

        buttons = []
        for grid_element in self.button_grid:
            # nested element can be a sub-grid (list with buttons)
            if list == type(grid_element) and 1 < len(grid_element):

                button_row = []
                for element in grid_element:
                    new_button = element.build()
                    button_row.append(new_button)
                buttons.append(button_row)

            # or single button (dict or singleton list of single button)
            elif issubclass(grid_element.__class__, Button) or is_singleton_list(grid_element):
                if list == type(grid_element):
                    grid_element = grid_element[0]

                new_button = grid_element.build()
                buttons.append([new_button])

            else:
                raise ValueError('Incorrect type of grid or sub-grid provided')

        kb = InlineKeyboardMarkup(buttons)
        return kb


class ViewTaskKb(Keyboard):
    def __init__(self, task_id, lang):
        super().__init__([
            [
                ViewTaskCommandButton('btn.view_task.mark_as_done.label', lang, Action.TASK_MARK_AS_DONE, data=task_id),
                ViewTaskCommandButton('btn.view_task.disable_notify.label', lang, Action.TASK_DISABLE, data=task_id),
                ViewTaskCommandButton('btn.view_task.delete_task.label', lang, Action.TASK_DELETE, data=task_id)
            ],
            [
                AllTasksCommandButton('btn.view_task.upcoming.label', lang, Action.LIST_UPCOMING),
                AllTasksCommandButton('btn.all_tasks.completed', lang, Action.LIST_COMPLETED),
                StartCommandButton('btn.all_tasks.home', lang)
            ]
        ])


class SelectLangKb(Keyboard):
    def __init__(self, lang):
        super().__init__([
            [
                SelectLangButton('btn.select_lang.eng.label', lang, lang_data=Language.ENG),
                SelectLangButton('btn.select_lang.rus.label', lang, lang_data=Language.RUS)
            ]
        ])


class StartStateKb(Keyboard):
    def __init__(self, lang):
        super().__init__([
            AllTasksCommandButton('btn.start_state.to_tasks.upcoming.label', lang, Action.LIST_UPCOMING),
            AllTasksCommandButton('btn.start_state.to_tasks.completed.label', lang, Action.LIST_COMPLETED),
            AllTasksCommandButton('btn.start_state.to_tasks.all.label', lang, Action.LIST_ALL),
            ViewLangCommandButton('btn.start_state.select_lang.label', lang, Action.VIEW_LANG)
        ])


class SelectProjectKb(Keyboard):
    def __init__(self, lang):
        super().__init__([
            [
                SelectProjectButton(lang, ProjectType.PERSONAL),
                SelectProjectButton(lang, ProjectType.STUDY),
                SelectProjectButton(lang, ProjectType.WORK),
                SelectProjectButton(lang, ProjectType.OTHER),
            ]
        ])


class TasksAsButtons(Keyboard):
    def __init__(self, tasks, lang):
        super().__init__(None)
        button_grid = []
        for task in tasks:
            btn_label = (':white_check_mark: ' if task.is_task_completed() else ':black_square_button: ') + task.get_description()

            task_as_button = ViewTaskCommandButton(btn_label, None, Action.TASK_VIEW, task.get_id())
            button_grid.append(task_as_button)

        # add navigation buttons
        # TODO add refresh button
        button_grid.append([
            AllTasksCommandButton('btn.all_tasks.upcoming', lang, Action.LIST_UPCOMING),
            AllTasksCommandButton('btn.all_tasks.completed', lang, Action.LIST_COMPLETED),
            StartCommandButton('btn.all_tasks.home', lang)
        ])
        self.set_button_grid(button_grid)
