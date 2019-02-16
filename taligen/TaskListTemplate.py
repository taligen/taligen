#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from taligen.TaskList import TaskList

class TaskListTemplate:
    """
    A parsed TaskListTemplate
    """
    def __init__( self, items, source ):
        """
        items: the steps in the template
        source: the file from which this was parsed
        """
        self.items  = items
        self.source = source;

    def get_source( self ):
        return self.source

    def instantiate( self, parameters, parser ):
        """
        Instantiate this Task List Template into a Task List,
        using the provided parameters. The parser is passed-on to
        sub-task-lists that might need it
        """
        steps = []
        localParameters = parameters.clone()

        for item in self.items:
            item.process( localParameters, steps, parser )

        return TaskList( steps, parameters, self );
