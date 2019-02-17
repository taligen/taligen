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
    def add_as_json( self, json_steps, step_id ):
        pass

    def with_context( self, json_content, step_id ):
        """
        Simplifies consistently adding the source information into
        the JSON by subclasses
        """
        ( source_file, source_line ) = self.template.get_source()

        json_content['source_file'] = source_file
        json_content['source_line'] = source_line
        json_content['id']          = step_id

        return json_content
