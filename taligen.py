#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#

import argparse
import re
import datetime
import json
import os
from collections import deque


def add_original_description(step, section, description):
    if section == "id":
        step["id"] = description
    else:
        ss = step.get(section, {})
        d = ss.get("raw_description", "")
        d += description
        ss["raw_description"] = d
        ss["description"] = d
        step[section] = ss
    return step


def add_comment(script, step, section, comment):
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


def add_step(steps, step, section):
    if section != "" or "comment" in step or "call" in step:
        steps.append(step)
    return steps


def arglist_to_paramdict(arglist):
    if isinstance(arglist, basestring):
        return arglist_to_paramdict(arglist.split(","))
    paramdict = {}
    for arg in arglist:
        if arg.strip() != '':
            splitlist = arg.split("=")
            paramdict[splitlist[0].strip()] = splitlist[1].strip()
    return paramdict


def params_to_string(substitutions):
    paramstring = ""
    for substitution in substitutions:
        paramstring += "," + substitution
    if paramstring != "":
        paramstring = "." + paramstring[1:]
    return paramstring


def read_through_file(filename, script, parsed_scripts, filestack):
    if filename in parsed_scripts:
        # print("found already parsed " + filename)
        return parsed_scripts[filename]

    if filename in filestack:
        print("recursion cycle: "
            + filename + " called when already in the stack: "
            + str(filestack))
        return ["recursion cycle: "
            + filename + " called when already in the stack: "
            + str(filestack)]

    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    steps = []
    step_num = 1
    step = {"id": str(step_num), "order": step_num}

    section = ""
    for line in lines:
        if line[0] == '#':
            add_comment(script, step, section, line)
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
                section = linematch.group(1).lower()
                description = linematch.group(2)
            else:
                description = "\n"+ line
            if linematch and section == "call":
                steps = add_step(steps, step, last_section)

                if last_section != "" or "comment" in step:
                    step_num += 1
                    step = {"id": str(step_num), "order": step_num}
                section = ""
                step["call"] = linematch.group(2)
                call_file_match = re.match("(.+)\((.*)\)\s*", linematch.group(2))
                call_file = call_file_match.group(1) + ".tl"
                step["name"] = call_file
                step["parameters"] = arglist_to_paramdict(call_file_match.group(2))
                filestack.append(filename)
                if os.path.dirname(filename) != '':
                    call_file = os.path.dirname(filename) + "/" + call_file
                step["steps"] = read_through_file(call_file, step,
                        parsed_scripts, filestack)
                filestack.pop()
                steps = add_step(steps, step, section)

                step_num += 1
                step = {"id": str(step_num), "order": step_num}
            else:
                add_original_description(step, section, description)
    steps = add_step(steps, step, section)
    parsed_scripts[filename] = steps
    return steps


def parse_arguments():
    argparser = argparse.ArgumentParser(description="taligen: generate json file from tl file")
    argparser.add_argument("tl_file", type=str, help=".tl (task list) file to generate from")
    argparser.add_argument("substitutions", type=str, nargs="*", help="substitutions to make in the file")
    return argparser.parse_args()


def collect_pass(args):
    script = {"name": args.tl_file}
    script["generated"] = str(datetime.datetime.now())
    script["parameters"] = arglist_to_paramdict(args.substitutions)
    script["steps"] = read_through_file(args.tl_file, script, {}, deque())
    return script


def replace_within_description(step, part, parameters):
    if part in step and len(parameters) > 0:
        for key, value in parameters.iteritems():
            step[part]["description"] = re.sub("\\$"+key, value, step[part]["description"])
    return step


def replace_pass(script, parameters):
    myparameters = parameters.copy()
    myparameters.update(script["parameters"])
    if len(myparameters) > 0:
        for step in script["steps"]:
            step = replace_within_description(step, "a", myparameters)
            step = replace_within_description(step, "o", myparameters)
            if "steps" in step:
                step = replace_pass(step, myparameters)
    return script


def main():
    args = parse_arguments()

    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    json_filename = dt+"."+os.path.splitext(args.tl_file)[0]+params_to_string(args.substitutions)+'.json'

    script = collect_pass(args)
    script["filename"] = json_filename
    script = replace_pass(script, {})

    with open(json_filename, 'w') as fp:
        json.dump(script, fp, indent=4)


main()
