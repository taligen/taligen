#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from taligen.SourceLocationStack import SourceLocationStack
from taligen.SubstitutionException import SubstitutionException
from taligen.SyntaxException import SyntaxException
from taligen.TaskListTemplateItem import TaskListTemplateItem

class TaskListTemplateSetItem(TaskListTemplateItem):
    """
    An item in a TaskListTemplate that, when instantiated, should set
    a parameter to a value.
    """
    def __init__( self, tag, content, tlt_loc ):
        super().__init__( tag, tlt_loc )

        self.content = content

    def process( self, parameters, items, parser, parentLocationStack ):
        try:
            inst_content = parameters.substitute( self.content )

        except KeyError as e:
            raise SubstitutionException( self.content, e.args[0], parameters, SourceLocationStack( self.tlt_loc, parameters, parentLocationStack ))

        ( key, value ) = inst_content.split( '=', 1 )
        if value is None:
            raise SyntaxException( 'Assignment is missing an =', self.tlt_loc )

        parameters.put( key, value )
