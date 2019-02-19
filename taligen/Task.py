#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class Task:
    """
    Abstract superclass of all items in a Task List
    """
    def __init__(self, template):
        """
        template: reference to the instance of (the subclass of)
             TaskListTemplateItem that this is an instance of
        """
        self.template = template
