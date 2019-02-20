#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import re

class TaskListParameters:
    """
    Collection of name-value pairs used for parameterizing TaskLists
    when instantiating TaskListTemplates
    """
    def __init__( self, pairs ):
        """
        pairs: the name-value pairs
        """
        self.pairs = pairs


    @staticmethod
    def from_string( s ):
        """
        Create from a key=value,key2=value2 string
        """
        return TaskListParameters.from_strings( re.split( '[,\s;]+', s ))


    @staticmethod
    def from_strings( ss ):
        """
        Create from a list of key=value strings
        """
        pairs = {}
        TaskListParameters.parse_strings( ss, pairs )
        return TaskListParameters( pairs )


    def add_from_string( self, s ):
        """
        Parse the string and add the found key-value pairs
        """
        TaskListParameters.parse_strings( re.split( '(?<!\\\\)[,\s;]+', s ), self.pairs )
        return self


    @staticmethod
    def parse_strings( ss, pairs ):
        """
        Static helped method to parse strings
        """
        for s in ss:
            s = s.strip()
            if s != '':
                splitlist = s.split("=", 1)
                if len(splitlist) >=2:
                    pairs[splitlist[0].strip()] = splitlist[1].strip()
                else:
                    raise ValueError( "Error: cannot split " + s + " into name=value")

    def __str__( self ):
        """
        Generate a param string: a => b, c => d becomes 'a=b.c=d'
        """
        ret = ''
        sep = ''

        for key, value in sorted(self.pairs.items()):
            ret += sep + key + '=' + value
            sep = '.'
        return ret

    def as_dict( self ):
        """
        Return as dictionary representation
        """
        return self.pairs

    def key_exists( self, key ):
        return key in self.pairs

    def get( self, key ):
        return self.pairs[key]

    def put( self, key, value ):
        self.pairs[key] = value

    def is_empty( self ):
        if self.pairs:
            return False
        else:
            return True

    def clone( self ) :
        return TaskListParameters( self.pairs.copy() )

    def substitute( self, s ):
        """
        Replace the variables in s with these parameters
        """
        last = 0
        ret  = ''
        for match in re.finditer( r"(?<=[^\\])\$(\w+)\b", s ):
            ret += s[last:match.start(0)]
            key = match.group(1)
            value = self.pairs[key]
            ret += value
            last = match.end(0)

        ret += s[last:]
        return ret
