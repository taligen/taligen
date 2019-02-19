#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class SourceLocation:
    """
    A particular location in a TLT source file
    """
    def __init__( self, filename, line ):
        self.filename = filename
        self.line     = line

    def __str__( self ):
        return self.filename + ", line " + str( self.line )
