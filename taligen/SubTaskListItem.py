#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from taligen.TaskListItem import TaskListItem

class SubTaskListItem(TaskListItem):
    """
    An item in a Task List that represents a subordinate Task List
    """
    def __init__(self, tl, template ):
        """
        tl: the subordinate instance of TaskList
        template: the TaskListTemplateCallItem of which this is an instance
        """
        super().__init__( template )

        self.tl = tl

    def as_json(self):
        ret = self.tl.as_json()
        ret['type'] = 'call'
        return ret
