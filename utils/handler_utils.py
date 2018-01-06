"""
Created by anthony on 15.10.17
handler_utils
"""
import json

from config.state_config import CommandType, CommandAliases, Action, CallbackData


def get_command_type(text):
    text = text.strip()
    if not text.startswith('/'):
        return CommandType.ECHO

    else:
        args = text.split()
        for command_type in CommandAliases.keys():
            for alias in CommandAliases.get(command_type):
                if alias == args[0]:
                    return command_type

        raise ValueError('Command not recognized')


def deserialize_data(data):
    """
    deserialize callback data into Action, CommandType, data
    """
    deserialized = json.loads(data)
    action = Action(deserialized[CallbackData.ACTION.value])
    command = CommandType(deserialized[CallbackData.COMMAND.value])
    data = deserialized[CallbackData.DATA.value]
    return {
        CallbackData.ACTION: action,
        CallbackData.COMMAND: command,
        CallbackData.DATA: data
    }


def is_callback(update):
    return update.callback_query is not None


def get_latest_list_action(actions):
    actions_to_be_found = [Action.LIST_ALL, Action.LIST_COMPLETED, Action.LIST_UPCOMING]

    actions_list = list(actions)
    i = len(actions_list) - 1
    while i >= 0:
        act = actions_list[i]
        if act in actions_to_be_found:
            return act

    return Action.LIST_ALL
