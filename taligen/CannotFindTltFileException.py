#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class CannotFindTltFileException(BaseException):
    """
    Thrown when a .tlt file cannot be found
    """
    def __init__( self, tlt, parameters, source = None, line = None ) :
        """
        We looked for file tlt, using parameters, and the problem
        occurred in file source at line line.
        """
        self.tlt        = tlt
        self.parameters = parameters
        self.source     = source
        self.line       = line

    def __str__( self ):
        ret =  'Cannot find tlt file ' + self.tlt
        if not self.parameters.is_empty():
            ret += ' with parameters ' + self.parameters.to_string()
        if self.source:
            ret += ' in file ' + self.source + ', line ' + str(self.line)

        return ret
