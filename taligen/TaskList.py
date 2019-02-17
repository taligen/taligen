#!/usr/bin/python
#
# An instance of a Task List Template
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class TaskList:
    """
    A Task List instantiated from a Task List Template, possibly with
    some parameters.
    """
    def __init__( self, steps, parameters, template ):
        """
        steps: the steps in the task list
        parameters: the parameters applied when instantiating the TaskList
        template: the TaskListTemplate of which this is an instance
        """
        self.steps       = steps
        self.parameters  = parameters
        self.template    = template

    def get_steps( self ):
        return self.steps

    def step_id( self, parent_id, local_child_id ):
        """
        Consistent creation of hierarchical ids
        """
        return parent_id + '.' + str( local_child_id )
