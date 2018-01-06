"""
Created by anthony on 21.11.2017
automata
"""
from collections import deque

from config.state_config import TRANSITION_TABLE, State, Language
from models.user import User
from utils import db_utils


CONTEXT_TASK = 'context_task'
CONTEXT_COMMANDS = 'context_commands'
CONTEXT_LANG = 'context_lang'
CONTEXT_ACTION = 'context_action'


class Automata:
    def __init__(self):
        self.user_to_state = {}
        self.user_to_context = {}


    def get_state(self, chat_id_value):
        chat_id = int(chat_id_value)
        if chat_id in self.user_to_state.keys():
            return self.user_to_state[chat_id]

        else:
            self.user_to_state[chat_id] = self.select_initial_state(chat_id)
            return self.user_to_state[chat_id]


    def set_state(self, chat_id, new_state):
        chat_id = int(chat_id)
        self.user_to_state[chat_id] = new_state
        return new_state


    @staticmethod
    def select_initial_state(chat_id):
        user_by_id = db_utils.find_one_by_id(chat_id, User)
        # if we already know this user then no need make him sign (/start) up again
        if user_by_id:
            return State.START

        else:
            return State.START


    def get_context(self, chat_id_value):
        chat_id = int(chat_id_value)
        if chat_id in self.user_to_context.keys():
            return self.user_to_context[chat_id]

        else:
            self.user_to_context[chat_id] = {
                # TODO keep whole view history (linked hash set deque-like)
                CONTEXT_TASK: None,
                CONTEXT_COMMANDS: deque(maxlen=10),
                CONTEXT_LANG: Language.ENG,
                CONTEXT_ACTION: deque(maxlen=10)
            }
            return self.user_to_context[chat_id]


    @staticmethod
    def if_can_transit_to(curr_state, command, new_state):
        allowed_state_id = TRANSITION_TABLE[curr_state][command]
        return allowed_state_id == new_state.value


    @staticmethod
    def get_transition(curr_state, command):
        # curr_state and command should instances of classes from above
        new_state_id = TRANSITION_TABLE[curr_state.value][command.value]
        return State(new_state_id)
