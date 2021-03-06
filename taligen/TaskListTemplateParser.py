#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import re
import os.path
from taligen.CannotFindTltFileException import CannotFindTltFileException
from taligen.SourceLocation import SourceLocation
from taligen.SubstitutionException import SubstitutionException
from taligen.SyntaxException import SyntaxException
from taligen.TaskListTemplate import TaskListTemplate
from taligen.TaskListTemplateCallItem import TaskListTemplateCallItem
from taligen.TaskListTemplateCheckboxItem import TaskListTemplateCheckboxItem
from taligen.TaskListTemplateErrorItem import TaskListTemplateErrorItem
from taligen.TaskListTemplateHeaderItem import TaskListTemplateHeaderItem
from taligen.TaskListTemplateSetItem import TaskListTemplateSetItem

class TaskListTemplateParser:
    """
    Knows how to parse TaskListTemplates and instantiate them as a
    a sequence of TaskListTemplateItems.
    """
    def __init__( self ):
        self.parsedFiles = {} # caches parsed files


    def find_tlt_file( self, tlt_file, parameters, context_path, locationStack ):
        """
        Find the most appropriate TLT file, given the provided filename
        (e.g. 'foo.tlt'), the current context (e.g. 'inc/sometfile.tlt'), and
        the parameters (e.g. 'abc=def').
        This might return 'inc/foo.abc=def.tlt'
        """
        if context_path:
            context_dir = os.path.dirname( context_path )
            tlt_file_base = context_dir + '/' + tlt_file if context_dir else tlt_file
        else:
            tlt_file_base = tlt_file

        (fdir, fname) = os.path.split(tlt_file_base)
        (fbase, fext) = os.path.splitext(fname)

        # We want the one in which the most parameters match, so we order by
        # the number of periods

        fbase_with_period = fbase + '.'

        candidates = list()
        dirs       = list()

        # for foo.tlt, look in its directory, and for foo/foo.tlt
        if fdir:
            dirs.append( fdir )
            if os.path.isdir( fdir + '/' + fbase ):
                dirs.append( fdir + '/' + fbase )
        else:
            dirs.append( '.' )
            if os.path.isdir( fbase ):
                dirs.append( fbase )

        for d in dirs:

            def filt(c):
                if not os.path.isfile( d + '/' + c ):
                    return False
                if not c.startswith( fbase_with_period ):
                    return False
                if not c.endswith( fext ): # contains period already
                    return False
                return True

            candidates += map(
                    lambda f: f if d == '.' else ( d + '/' + f ),
                    filter( filt, os.listdir( d )))

        found = None

        def candidateQuality(c):
            # Prefer fewer dots, but in doubt, shorter directories
            # (that's where the times 2 comes from)
            lastSlash = c.rfind( '/' )
            if lastSlash == -1:
                return -c.count( '.' ) * 2
            else:
                return -c.count( '.', lastSlash + 1 ) * 2 + 1

        sortedCandidates = sorted( candidates, key=candidateQuality )

        for candidate in sortedCandidates:

            # The first one that matches parameters is the best match
            lastSlash = candidate.rfind( '/' )
            if lastSlash == -1:
                pairs = candidate[ len( fbase_with_period ) : -len( fext ) ]
            else:
                pairs = candidate[ lastSlash + 1 + len( fbase_with_period ) : -len( fext ) ]

            if( len( pairs )):
                matched_all = True
                for pair in pairs.split( '.' ):
                    try :
                        ( key, value ) = pair.split( '=', 1 )
                    except ValueError as e:
                        print( 'Cannot split supposed key-value pair: ' + pair )
                        raise e

                    # all of them have to match
                    if( not parameters.key_exists( key ) or parameters.get( key ) != value ):
                        matched_all = False
                        break
                if matched_all:
                    found = candidate
                    break

        if found == None:
            # Is there one with no parameters?
            for candidate in sortedCandidates:
                lastSlash = candidate.rfind( '/' )
                if lastSlash == -1:
                    if candidate == fname:
                        found = tlt_file_base
                else:
                    if candidate[ lastSlash+1 : ] == fname:
                        found = candidate

            if found == None:
                raise CannotFindTltFileException( tlt_file_base, parameters, locationStack )

        return os.path.normpath( found )


    def obtain_with_parameters( self, tlt_file_base, parameters, path, locationStack ):
        """
        Find the correct TLT file given the path and the parameters,
        and return a parsed version of it
        """
        tlt_file = self.find_tlt_file( tlt_file_base, parameters, path, locationStack )
        if tlt_file:
            return self.obtain( tlt_file )
        else:
            return None


    def obtain( self, tlt_file ):
        """
        Smartly parses the file, and returns a parsed version of it
        """
        ret = self.parsedFiles.get(tlt_file,None)
        if ret is None:
            ret = self.parse( tlt_file )
            self.parsedFiles[tlt_file] = ret

        return ret


    def parse( self, tlt_file ):
        """
        Parses the file, and returns a parsed version of it.
        """
        if not os.path.isfile( tlt_file ):
            raise ValueError( 'File does not exist: ' + tlt_file )

        f  = open( tlt_file, "r")
        lines = f.readlines() # may throw exception
        f.close()

        # consolidate lines and parse them
        current      = None # build up consolidated line here
        line_count   = 0
        items        = []

        def syntaxError( msg ):
            """
            Helper method to raise a syntax error
            """
            raise SyntaxException( msg, SourceLocation( tlt_file, line_count ))

        def parseConsolidatedLine( line ):
            """
            After continuation lines have been consolidated, parse this
            consolidated line
            """
            ( tag, content ) = line.split( ':', 1 )

            tag     = tag.lower()
            content = content.strip()
            tlt_loc = SourceLocation( tlt_file, line_count )

            if content is None:
                syntaxError( 'No tag present' )
            elif tag in [ 'a', 'o' ]:
                items.append( TaskListTemplateCheckboxItem( tag, content, tlt_loc ))
            elif tag == 'h':
                items.append( TaskListTemplateHeaderItem( tag, content, tlt_loc ))
            elif tag == 'set':
                items.append( TaskListTemplateSetItem( tag, content, tlt_loc ))
            elif tag == 'call':
                items.append( TaskListTemplateCallItem( tag, content, tlt_loc ))
            elif tag == 'error':
                items.append( TaskListTemplateErrorItem( tag, content, tlt_loc ))
            else:
                syntaxError( 'Unknown tag ' + tag )


        for line in lines:
            line_count += 1

            line = re.sub( '\s+$', '',  line ) # trim trailing blanks
            line = re.sub( '^\s+', ' ', line ) # trim leading blanks except one
            line = re.sub( '#.*' , '',  line ) # strip comments

            if line:
                if line[0] == ' ':
                    # continuation line
                    if current == None:
                        syntaxError( 'Invalid leading space in non-continuation line' )
                    else:
                        current += line # including leading blank

                elif current != None:
                    # new item
                    parseConsolidatedLine( current )
                    current = line

                else:
                    current = line

            elif current != None:
                parseConsolidatedLine( current )
                current = None

        if current:
            parseConsolidatedLine( current )

        return TaskListTemplate( items, tlt_file )
