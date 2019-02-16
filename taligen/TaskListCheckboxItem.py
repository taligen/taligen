#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from taligen.TaskListItem import TaskListItem

class TaskListCheckboxItem(TaskListItem):
    """
    A TaskListItem that will be rendered with a checkbox
    """
    def __init__(self, content, template):
        super().__init__( template )

        self.content = content

    def as_json(self):
        return {
            'type'    : self.template.tag,
            'content' : self.content
        }


