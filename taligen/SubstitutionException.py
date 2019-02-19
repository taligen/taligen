#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from taligen.SourceLocation import SourceLocation

class SubstitutionException(BaseException):
    """
    Thrown when a variable substitution could not be made
    """
    def __init__( self, content, var, parameters, locationStack ) :
        """
        The content contains the variables, var was not found, parameters
        are the available parameters, and loc where the problem occurred
        """
        self.content       = content
        self.var           = var
        self.parameters    = parameters
        self.locationStack = locationStack

    def __str__( self ):
        ret = 'Could not substitute "' + self.var + '"' + " at:\n"
        ret += str( self.locationStack )
        return ret
