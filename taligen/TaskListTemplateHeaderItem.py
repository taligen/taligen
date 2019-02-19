#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from taligen.SourceLocationStack import SourceLocationStack
from taligen.SubstitutionException import SubstitutionException
from taligen.TaskListHeaderItem import TaskListHeaderItem
from taligen.TaskListTemplateItem import TaskListTemplateItem

class TaskListTemplateHeaderItem(TaskListTemplateItem):
    """
    An item in a TaskListTemplate that, when instantiated, should be
    rendered as a header
    """
    def __init__( self, tag, content, tlt_loc ):
        super().__init__( tag, tlt_loc )

        self.content = content

    def process( self, parameters, items, parser, parentLocationStack ):
        try:
            inst_content = parameters.substitute( self.content )

        except KeyError as e:
            raise SubstitutionException( self.content, e.args[0], parameters, SourceLocationStack( self.tlt_loc, parameters, parentLocationStack ))

        items.append( TaskListHeaderItem( inst_content, self ))
