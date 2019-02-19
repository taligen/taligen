#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import abc

class TaskListTemplateItem:
    def __init__( self, tag, tlt_loc ):
        """
        Abstract superclass of all items that can be on a Task List Template
        tag: the tag of the item, such as "a" or "call"
        content: the actual invocation
        tlt_loc: the location in the source where the item was foudn
        """
        self.tag     = tag.lower() # normalize
        self.tlt_loc = tlt_loc

    def get_location( self ):
        return ( self.tlt_loc )

    @abc.abstractmethod
    def process( self, parameters, items, parser, parentLocationStack ):
        """
        Do whatever necessary to process this item with respect to
        the provided sequence of previously processed TaskListItems
        """
        pass
