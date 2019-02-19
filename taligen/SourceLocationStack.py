#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class SourceLocationStack:
    """
    Stack<SourceLocation> that keeps context for TaskListTemplate
    instantiation. This implements a stack by pointing to the parent
    SourceLocationStack.
    """
    def __init__( self, loc, parameters, parent = None ):
        self.loc        = loc
        self.parameters = parameters
        self.parent     = parent

    def peek( self ):
        return self.loc

    def __str__( self ):
        ret = str( self.loc )

        if not self.parameters.is_empty() :
            ret += ' (' + str( self.parameters ) + ')'

        if self.parent:
            ret += "\n" + str( self.parent )
        return ret
