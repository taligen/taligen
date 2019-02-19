#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class SyntaxException(BaseException):
    """
    Invalid syntax in a source file
    """
    def __init__( self, msg, loc ) :
        """
        Detailed message msg, problem occurred in file source at line
        line
        """
        self.msg = msg
        self.loc = loc

    def __str__( self ):
        return 'Syntax error: ' + self.msg + '" at ' + str(self.loc)
