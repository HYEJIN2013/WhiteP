#!/usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################
# Check out more of my .dotfiles at github.com/jstarry/dotfiles
#
# Required: colorama -- Install using $ pip install colorama
#
# Pro Tip: alias git branch to "!python git-tree.py"
####################################################################

import subprocess
import re
from colorama import Fore, Back
import sys

tracking_regex = re.compile(r'([a-zA-Z][a-zA-Z0-9\-_\/]*)\s+([a-f0-9]+)\s+\[(.+)\]\s+(.+)')
untracking_regex = re.compile(r'([a-zA-Z][a-zA-Z0-9\-_\/]*)\s+([a-f0-9]+)\s+(.+)')

class Branch:
    def __init__(self, name, commit_hash, commit_msg, current, tracking = None, ahead = 0, behind = 0, broken = False):
        self.name = name
        self.commit_hash = commit_hash
        self.commit_msg = commit_msg
        self.current = current
        self.tracking = tracking
        self.ahead = ahead
        self.behind = behind
        self.branches = []
        self.parent = None
        self.last = False
        self.broken = broken
        self.indent_string = ''
    def __str__(self):
        prefix_length = self.indent * 4 + len(self.name) + 1
        branch_str = self.indent_string
        if self.current:
            branch_str += Back.YELLOW + Fore.BLACK
        else:
            branch_str += Fore.YELLOW
        branch_str += self.name + Fore.RESET + Back.RESET
        branch_str += ' ' * (maxPrefix - prefix_length)
        branch_str += " " + self.commit_hash
        if self.tracking is not None:
            branch_str += " [" + Fore.BLUE + self.tracking + Fore.RESET
            if self.ahead > 0 or self.behind > 0:
                branch_str += ":"
                if self.ahead > 0:
                    branch_str += " ahead " + str(self.ahead)
                    if self.behind > 0:
                        branch_str += ","
                if self.behind > 0:
                    branch_str += " behind " + str(self.behind)
            if self.broken:
                branch_str += ": gone"
            branch_str += "]"
        branch_str += " " + self.commit_msg
        return branch_str
    def __gt__(self, other):
        return self.name > other.name

def parseTrackingBranch(current, match):
    name = match.group(1)
    commit_hash = match.group(2)
    commit_msg = match.group(4)
    ahead_count = 0
    behind_count = 0
    broken = False

    tracking_info = match.group(3).split(':')
    tracking_branch = tracking_info[0]
    if len(tracking_info) > 1:
        tracking_status = tracking_info[1].split(',')
        for status in tracking_status:
            status = status.split()
            status_type = status[0]
            if status_type == 'gone':
                broken = True
                break
            status_count = status[1]
            if status_type == 'ahead':
                ahead_count = int(status_count)
            else:
                behind_count = int(status_count)
    return Branch(name, commit_hash, commit_msg, current, tracking_branch, ahead_count, behind_count, broken)

def parseUntrackingBranch(current, match):
    name = match.group(1)
    commit_hash = match.group(2)
    commit_msg = match.group(3)
    return Branch(name, commit_hash, commit_msg, current)

def parse(line):
    current = False
    line = line.strip()
    if (line[0] == '*'):
        current = True
        line = line[2:]

    match = re.match(tracking_regex, line)
    if match:
        return parseTrackingBranch(current, match)
    match = re.match(untracking_regex, line)
    if match:
        return parseUntrackingBranch(current, match)

    print 'Could not parse this line:\n' + line

def removeNones(branches):
    return [x for x in branches if x is not None]

def process(branches):
    mapping = {}
    root_branches = []
    for branch in branches:
        mapping[branch.name] = branch
    for branch in branches:
        if branch.tracking is None or branch.tracking.find('origin/') >= 0 or branch.broken:
            root_branches.append(branch)
        else:
            mapping[branch.tracking].branches.append(branch)
            branch.parent = mapping[branch.tracking]
    for branch in branches:
        if len(branch.branches) > 0:
            branch.branches[-1].last = True
    return root_branches

indent_up = '└── '
indent_line = '│   '
indent_space = '    '
indent_connector = '├── '
    
def createIndentString(branch, indent):
    indent_string = ''
    if branch.parent is not None:
        if branch.last is True:
            indent_string = indent_up
        else:
            indent_string = indent_connector
        tmp_branch = branch.parent
        while tmp_branch.parent is not None:
            if tmp_branch.last is True:
                indent_string = indent_space + indent_string
            else:
                indent_string = indent_line + indent_string
            tmp_branch = tmp_branch.parent
        indent_string = '    ' + indent_string
    branch.indent_string = indent_string
    if indent > 0:
        branch.indent = indent + 1
    else:
        branch.indent = indent
    for sub_branch in branch.branches:
        createIndentString(sub_branch, indent + 1)

def printBranch(branch):
    print branch
    for sub_branch in branch.branches:
        printBranch(sub_branch)

lines = subprocess.check_output(["git", "branch", "-vv"]).splitlines()
branches = removeNones(map(parse, lines))
root_branches = process(branches)
for branch in root_branches:
    createIndentString(branch, 0)
maxPrefix = 0
for branch in branches:
    maxPrefix = max(maxPrefix, branch.indent * 4 + len(branch.name) + 1)
for branch in root_branches:
    printBranch(branch)
