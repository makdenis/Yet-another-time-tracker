"""
Created by anthony on 07.12.2017
abstract_entity
"""


class AbstractEntity:
    def __init__(self):
        # safe delete flag
        self.is_active = True

    def mark_as_active(self):
        self.is_active = True

    def mark_as_inactive(self):
        self.is_active = False

    def is_flag_active(self):
        return self.is_active
