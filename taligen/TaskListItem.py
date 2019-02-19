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

    def get_name( self ):
        """
        By default, TaskListItems do not have names, except that
        TaskLidHeaderItem does.
        """
        return None

    @abc.abstractmethod
    def add_as_json( self, json_steps, step_id ):
        pass

    def with_context( self, json_content, step_id ):
        """
        Simplifies consistently adding the source information into
        the JSON by subclasses
        """
        loc = self.template.get_location()

        json_content['source_file'] = loc.filename
        json_content['source_line'] = loc.line
        json_content['id']          = step_id

        return json_content
