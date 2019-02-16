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

    def as_json( self ):
        ret = {
            'template'   : self.template.get_source(),
            'parameters' : self.parameters.as_dict(),
            'steps'      : list( map( lambda s: s.as_json(), self.steps ))
        }
        return ret
