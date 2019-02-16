#!/usr/bin/python
#
# Abstract superclass of all items in a Task List
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import abc

class TaskListItem:
    """
    An abstract item on a Task List
    """
    def __init__(self, template):
        """
        template: the TaskListTemplateItem of which this is an instance
        """
        self.template = template

    @abc.abstractmethod
    def as_json(self):
        pass
