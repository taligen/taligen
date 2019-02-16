#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class Task:
    """
    Abstract superclass of all items in a Task List
    """
    def __init__(self, task_template):
        """
        task_template: reference to the instance of (the subclass of)
             TaskTemplate that this is an instance of
        """
        self.template = task_template
