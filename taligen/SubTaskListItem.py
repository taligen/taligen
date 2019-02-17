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

    def add_as_json( self, json_steps, step_id = '' ):
        index = 0
        for sub_step in self.tl.get_steps():
            index += 1
            sub_step.add_as_json( json_steps, self.tl.step_id( step_id, index ))

