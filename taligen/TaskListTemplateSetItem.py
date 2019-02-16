#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from taligen.TaskListTemplateItem import TaskListTemplateItem
from taligen.SubstitutionException import SubstitutionException
from taligen.SyntaxException import SyntaxException

class TaskListTemplateSetItem(TaskListTemplateItem):
    """
    An item in a TaskListTemplate that, when instantiated, should set
    a parameter to a value.
    """
    def __init__( self, tag, content, tlt_file, line_number ):
        super().__init__( tag, tlt_file, line_number )

        self.content = content

    def process( self, parameters, items, parser ):
        try:
            inst_content = parameters.substitute( self.content )

        except KeyError as e:
            raise SubstitutionException( self.content, e.args[0], parameters, self.tlt_file, self.line_number )

        ( key, value ) = inst_content.split( '=', 1 )
        if value is None:
            raise SyntaxException( 'Assignment is missing an =', tlt_file, line_number )

        parameters.put( key, value )
