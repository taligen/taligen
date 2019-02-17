#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import abc

class TaskListTemplateItem:
    def __init__( self, tag, tlt_file, line_number ):
        """
        Abstract superclass of all items that can be on a Task List Template
        tag: the tag of the item, such as "a" or "call"
        content: the actual invocation
        tlt_file: the file in which this item was found
        line_number: the line number at which this item was found
        """
        self.tag         = tag
        self.tlt_file    = tlt_file
        self.line_number = line_number

    def get_source( self ):
        return ( self.tlt_file, self.line_number )

    @abc.abstractmethod
    def process( self, parameters, items, parser ):
        """
        Do whatever necessary to process this item with respect to
        the provided sequence of previously processed TaskListItems
        """
        pass
