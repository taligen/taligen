#!/usr/bin/python
#
# Setup the package.
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import argparse
import datetime
import json
import os
import sys
from taligen.TaskListParameters import TaskListParameters
from taligen.TaskListTemplateParser import TaskListTemplateParser
from taligen.CannotFindTltFileException import CannotFindTltFileException
from taligen.SyntaxException import SyntaxException
from taligen.SubstitutionException import SubstitutionException

def run():
    """
    Main program

    taligen.py [ --output <file> | --output-directory <dir> ] <tltfile> [ <par> ...]
    """

    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    argparser = argparse.ArgumentParser(description="taligen: generate json task list file from .tlt file and files called from there")
    argparser.add_argument("tlt_file",                 type=str,                   help=".tlt (task list template) file to generate from")
    argparser.add_argument("parameters",               type=str, nargs="*",        help="parameters to substitute for variables in the .tlt files")
    argparser.add_argument("-o", "--output",           type=str,                   help="output filename (optional)")
    argparser.add_argument("-O", "--output-directory", type=str, dest='outputDir', help="output directory (optional)")

    args = argparser.parse_args()

    tlt_file   = args.tlt_file;
    parameters = TaskListParameters.from_strings( args.parameters )

    if args.output:
        if args.outputDir:
            raise ValueError( 'Specify --output or --output-directory, not both' )

        json_filename = args.output

    elif args.outputDir:
        json_filename = re.sub('.tlt$', '', tlt_file) # if it ends in .tlt, strip
        json_filename = re.sub('^.*/', '', json_filename) # strip directory
        json_filename = json_filename + '.json'
        if (args.outputDir.endswith('/')):
            json_filename = args.outputDir + json_filename
        else:
            json_filename = args.outputDir + '/' + json_filename
    else:
        json_filename = None

    parser = TaskListTemplateParser()

    try:
        tlt = parser.obtain_with_parameters( args.tlt_file, parameters )
        tl = tlt.instantiate( parameters, parser )

        json_content = {
            'template'   : tl.template.get_source(),
            'parameters' : tl.parameters.as_dict(),
            'steps'      : []
        }
        index = 0
        for step in tl.get_steps():
            index += 1
            step.add_as_json( json_content['steps'], str(index) )

        if json_filename:
            with open(json_filename, 'w') as fp:
               json.dump( json_content, fp, indent=2)
            print("Generated " + json_filename)
        else:
            print( json.dumps( json_content, indent=2 ))

    except SubstitutionException as e:
        exit( 'FATAL: ' + str( e ))
    except SyntaxException as e:
        exit( 'FATAL: ' + str( e ))
    except CannotFindTltFileException as e:
        exit( 'FATAL: ' + str( e ))


if __name__ == "__main__":
    run()
