#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#

import argparse
import re
import datetime
import json
import os
import sys
import copy
from collections import deque


def add_original_description(step, section, description):
    if section == "id":
        step["id"] = description
    else:
        ss = step.get(section, {})
        d = ss.get("raw_description", "")
        if d == "":
            d = description
        else:
            d += "<br>" + description
        ss["raw_description"] = d
        ss["description"] = d
        step[section] = ss
    return step


def add_comment(step, section, comment):
    if section == "":
        c = step.get("comment", "")
        step["comment"] = c + comment
    else:
        ss = step.get(section, {})
        c = ss.get("comment", "")
        c += comment
        ss["comment"] = c
        step[section] = ss
    return step


def add_error(step, section, error):
    if section == "":
        c = step.get("error", "")
        step["error"] = c + error
    else:
        ss = step.get(section, {})
        c = ss.get("error", "")
        c += error
        ss["error"] = c
        step[section] = ss
    return step


def add_step(steps, step, section):
    if section != "" or "comment" in step or "call" in step or "set" in step or "error" in step:
        steps.append(step)
    return steps


def arglist_to_paramdict(arglist):
    if isinstance(arglist, str):
        return arglist_to_paramdict(arglist.split(","))
    paramdict = {}
    for arg in arglist:
        arg = arg.strip()
        if arg != '':
            splitlist = arg.split("=")
            if len(splitlist) >=2:
                paramdict[splitlist[0].strip()] = splitlist[1].strip()
            else:
                exit( "Error: cannot split "+arg+" into name=value")
    return paramdict


def params_to_string(substitutions):
    paramstring = ""
    for substitution in substitutions:
        paramstring += "," + substitution
    if paramstring != "":
        paramstring = "." + paramstring[1:]
    return paramstring


def find_parameterized_file(path, filename, parameters, filestack):
    (fdir, fname) = os.path.split(filename)
    (fbase, fext) = os.path.splitext(fname)
    # print ("\n\nfind_parameterized_file at " + path + " " + filename + "(" + fdir + ", " + fbase + ", " + fext + ") " + "  " + str(parameters))
    if fdir == "":
        # print ("    fdir is empty string")
        fdir = path
    else:
        fdir = path + "/" + fdir
    f = {}
    for (dirpath, dirnames, filenames) in os.walk(fdir):
        # f.extend(filenames)
        # print ("dirpath: " + dirpath + ", dirnames: " + str(dirnames) + ", filenames: " + str(filenames))
        for ffname in filenames:
            if ffname.startswith(fbase + "."):
                file_args = os.path.splitext(ffname)[0][len(fbase)+1:]
                # print("... looking at  " + ffname + " in " + dirpath + " with arglist " + file_args)
                argdict = arglist_to_paramdict(file_args)
                match = True
                for arg in argdict:
                    if not arg in parameters or parameters[arg] != argdict[arg]:
                        match = False
                if match:
                    f[ffname] = len(argdict)
        break
    # print ("choices are: " + str(f))
    if len(f) == 0:
        exit("Error:  File "+filename+" not found.  Callstack is: "+ str(filestack) + " Paramaters are: "+ str(parameters))
        
    maxargs = -1
    chosenfile = ""
    for name in f:
        if f[name] > maxargs:
            chosenfile = name
            maxargs = f[name]
    # print ("chose  " + fdir + "/" + chosenfile)
    return fdir + "/" + chosenfile


def get_file_lines(pfilename, parsed_scripts, filestack):
    if pfilename in filestack:
        exit("Error:  Recursion cycle: "
            + pfilename + " called when already in the stack: "
            + str(filestack))

    lines = []
    try:
      file = open(pfilename, "r")
      lines = file.readlines()
      file.close()
    except Exception as e:
        exit("Error:  Error reading file " + pfilename + " -- " + str(e))

    return lines


def read_through_file(path, filename, parameters, parsed_scripts, filestack):
    # print ("reading in " + path + " through " + filename + "(" + str(parameters) + ") from  " + str(filestack))
    if os.path.split(filename)[0] != "":
        path = path + "/" + os.path.split(filename)[0]
        filename = os.path.split(filename)[1]
    
    pfilename = find_parameterized_file(path, filename, parameters, filestack)

    if pfilename in parsed_scripts:
        # print("found already parsed " + pfilename)
        return copy.deepcopy(parsed_scripts[pfilename])

    # print("parmeterized filename is " + pfilename)
    lines = get_file_lines(pfilename, parsed_scripts, filestack)

    steps = []
    step_num = 1
    step = {"id": str(step_num), "order": step_num}

    section = ""
    for line in lines:
        if line[0] == '#':
            add_comment(step, section, line)
        elif line.strip() == '':
            steps = add_step(steps, step, section)
            if section != "" or "comment" in step:
                step_num += 1
                step = {"id": str(step_num), "order": step_num}
            section = ""
        else:
            last_section = section
            linematch = re.match("([A-Za-z]+):\s*(.*)", line)
            if linematch:
                steps = add_step(steps, step, last_section)

                if last_section != "" or "comment" in step:
                    step_num += 1
                    step = {"id": str(step_num), "order": step_num}

                section = linematch.group(1).lower()
                description = linematch.group(2)
            else:
                description = line
            if linematch and section == "set":
                section = ""
                
                set_param_match = re.match("\s*(.+)\s*=\s*(.+)\s*", linematch.group(2))
                parameter = set_param_match.group(1)
                value = set_param_match.group(2)
                step["set"] = {"parameter": parameter, "value": value}
                if not parameter in parameters:
                    parameters[parameter] = value
                    # print ("added parameter: " + parameter + ", value: " + value)
                steps = add_step(steps, step, section)
                
                step_num += 1
                step = {"id": str(step_num), "order": step_num}                
            elif linematch and section == "call":
                section = ""
                
                step["call"] = linematch.group(2)
                # print("call found  " + step["call"])
                call_file_match = re.match("(.+)\((.*)\)\s*", linematch.group(2))
                if not call_file_match:
                    exit("Error: Incorrect call syntax in step " + step["id"] + " '" + line + "' call stack is " + str(filestack))
                call_file = call_file_match.group(1) + ".tl"
                step["name"] = call_file
                call_parameters = parameters.copy()
                # print("  call_parameters1: " + str(call_parameters))
                # print("  call file match 1: " + str(call_file_match.group(1)))
                # print("  call file match 2: " + str(call_file_match.group(2)))
                # print("  call file params: " + str(arglist_to_paramdict(call_file_match.group(2))))
                call_parameters.update(arglist_to_paramdict(call_file_match.group(2)))
                # print("  call_parameters2: " + str(call_parameters))
                # call_parameters = {**parameters, **arglist_to_paramdict(call_file_match.group(2))}
                filestack.append(pfilename)
                # print("... setting step filename ")
                step["filename"] = find_parameterized_file(path, call_file, call_parameters, filestack)
                # step["parameters"] = arglist_to_paramdict(call_file_match.group(2))
                step["parameters"] = call_parameters
                # print("call step added " + pfilename + " to " + str(filestack))
                step["steps"] = read_through_file(path, call_file, call_parameters, 
                        parsed_scripts, filestack)
                filestack.pop()
                steps = add_step(steps, step, section)

                step_num += 1
                step = {"id": str(step_num), "order": step_num}
            else:
                add_original_description(step, section, description)
    steps = add_step(steps, step, section)
    parsed_scripts[pfilename] = steps
    return steps


def parse_arguments():
    argparser = argparse.ArgumentParser(description="taligen: generate json file from tl file")
    argparser.add_argument("tl_file", type=str, help=".tl (task list) file to generate from")
    argparser.add_argument("parameters", type=str, nargs="*", help="parameters to substitute for variables in the .tl files")
    argparser.add_argument("-o", "--output", type=str, help="output filename (optional)")
    argparser.add_argument("-O", "--output-directory", type=str, dest='outputDir', help="output directory (optional)")
    return argparser.parse_args()


def collect_pass(args):
    script = {"name": args.tl_file}
    script["generated"] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    script["parameters"] = arglist_to_paramdict(args.parameters)
    script["steps"] = read_through_file(".", args.tl_file, script["parameters"], {}, deque())
    return script


def replace_within_description(step, part, parameters, filestack):
    # print("... replace_within_description: " + part + " " + str(filestack))
    if isinstance(step, dict) and part in step and len(parameters) > 0:
        # print("...... description: " + step[part]["description"])
        for key, value in parameters.items():
            # print("...... $" + key + " -> " + value)
            step[part]["description"] = re.sub("\\$"+key, value, step[part]["description"])
        set_vars = re.findall(r"\$\w+", step[part]["description"])
        for var in set_vars:
            # print("Missing " + var[1:] + " for " + step[part]["description"])
            # step["comment"] = step.get("comment", "") + "\nMissing " + var[1:] + " for " + step[part]["description"]
            # return add_error(step, part, "Missing " + var[1:] + " for " + step[part]["description"])
            exit("Error: Missing value for variable " + var[1:] + " for step " + step["id"] + " " + part + " " + step[part]["description"] + " call stack is " + str(filestack))
    return step


def replace_pass(script, parameters, filestack):
    # print("replace pass: filename: "+ script["filename"] + ", context parameters: " + str(parameters) + ", script parameters: " + str(script["parameters"]))
    myparameters = parameters.copy()
    # print("... myparameters: " + str(myparameters))
    myparameters.update(script["parameters"])
    # print("...... myparameters: " + str(myparameters))

    for step in script["steps"]:
        step = replace_within_description(step, "a", myparameters, filestack)
        step = replace_within_description(step, "o", myparameters, filestack)
        if "steps" in step:
            filestack.append(step["filename"]+"("+str(step["parameters"])+")")
            step = replace_pass(step, myparameters, filestack)
            filestack.pop()
    return script


def main():
    args = parse_arguments()

    tl_file = args.tl_file;
    if (args.output):
        json_filename = args.output
    elif (args.outputDir):
        json_filename = re.sub('.tl$', '', tl_file) # if it ends in .tl, strip
        json_filename = re.sub('^.*/', '', json_filename) # strip directory
        if (args.outputDir.endswith('/')):
            json_filename = args.outputDir + json_filename + '.json'
        else:
            json_filename = args.outputDir + '/' + json_filename + '.json'
    else:
        dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        json_filename = dt+"."+os.path.splitext(os.path.basename(args.tl_file))[0]+params_to_string(args.parameters)+'.json'

    script = collect_pass(args)
    script["filename"] = json_filename
    script = replace_pass(script, {}, [args.tl_file+"("+str(args.parameters)+")"])

    with open(json_filename, 'w') as fp:
        json.dump(script, fp, indent=4)
    print("Generated " + json_filename + " from " + args.tl_file)


main()
