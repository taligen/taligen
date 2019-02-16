#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class SubstitutionException(BaseException):
    """
    Thrown when a variable substitution could not be made
    """
    def __init__( self, content, var, parameters, source, line ) :
        """
        The content contains the variables, var was not found, parameters
        are the available parameters, and the problem occurred at tlt
        file source, line line.
        """
        self.content    = content
        self.var        = var
        self.parameters = parameters
        self.source     = source
        self.line       = line

    def __str__( self ):
        return 'Could not substitute "' + self.var + '" in file ' + self.source + ', line ' + str(self.line)
