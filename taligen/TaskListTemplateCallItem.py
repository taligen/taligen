#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import re
from taligen.TaskListTemplateItem import TaskListTemplateItem
from taligen.SubstitutionException import SubstitutionException
from taligen.SubTaskListItem import SubTaskListItem
from taligen.SyntaxException import SyntaxException

class TaskListTemplateCallItem(TaskListTemplateItem):
    """
    An item in a Task List Template that references another Task List
    Template as a "subroutine", possibly with additional parameters
    """
    def __init__( self, tag, content, tlt_file, line_number ):
        super().__init__( tag, tlt_file, line_number )

        self.content = content

    def process( self, parameters, items, parser ):
        try:
            inst_content = parameters.substitute( self.content )

        except KeyError as e:
            raise SubstitutionException( self.content, e.args[0], parameters, self.tlt_file, self.line_number )

        match = re.search( '^([^()]+)\(([^()]*)\)$', inst_content );
        if not match:
            raise SyntaxException( 'Invalid call syntax: ' + self.content, self.tlt_file, self.line_number )

        function = match.group( 1 ).strip()
        args     = match.group( 2 ).strip()

        child_parameters = parameters.clone();
        child_parameters.add_from_string( args )

        tlt = parser.obtain_with_parameters( function + '.tlt', child_parameters, self.tlt_file )
        if tlt:
            tl = tlt.instantiate( child_parameters, parser )
            items.append( SubTaskListItem( tl, self ))
