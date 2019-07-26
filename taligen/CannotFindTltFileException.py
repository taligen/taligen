#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class CannotFindTltFileException(BaseException):
    """
    Thrown when a .tlt file cannot be found
    """
    def __init__( self, tlt, parameters, locationStack) :
        """
        We looked for file tlt, using parameters,
        and loc where the problem occurred
        """
        self.tlt           = tlt
        self.parameters    = parameters
        self.locationStack = locationStack


    def __str__( self ):
        ret =  'Cannot find tlt file ' + self.tlt
        if not self.parameters.is_empty():
            ret += ' with parameters ' + str( self.parameters )
        ret += "\n" + str( self.locationStack )

        return ret
