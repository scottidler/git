#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import argparse
import importlib

sys.dont_write_bytecode = True

from importlib.machinery import SourceFileLoader
from subprocess import CalledProcessError

from git import clone

REAL_FILE = os.path.abspath(__file__)
REAL_NAME = os.path.basename(REAL_FILE)
REAL_PATH = os.path.dirname(REAL_FILE)
if os.path.islink(__file__):
    LINK_FILE = REAL_FILE; REAL_FILE = os.path.abspath(os.readlink(__file__))
    LINK_NAME = REAL_NAME; REAL_NAME = os.path.basename(REAL_FILE)
    LINK_PATH = REAL_PATH; REAL_PATH = os.path.dirname(REAL_FILE)

REMOTES = [
    "ssh://git@github.com",
    "https://github.com"
]

def discover(repospec, verbose=False):
    for remote in REMOTES:
        if verbose:
            print(f'remote = {remote}')
        repourl = os.path.join(remote, repospec)
        if verbose:
            print(f'repourl = {repourl}')
        exitcode, stdout, stderr = git.ls_remote(repourl, throw=False, verbose=verbose)
        if 0 == exitcode:
            return remote, repospec
    return None, None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--clonepath',
        metavar='PATH',
        default=os.getcwd(),
        help='path to store all cloned repos')
    parser.add_argument(
        '--mirrorpath',
        metavar='PATH',
        help='path to cached repos to support fast cloning')
    parser.add_argument(
        '--versioning',
        action='store_true',
        help='turn on versioning; checkout in reponame/commit rather than reponame')
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='turn on verbose output')
    parser.add_argument(
        'repospec',
        help='repospec schema is remote?reponame')
    parser.add_argument(
        'revision',
        default='HEAD',
        nargs='?',
        help='revision')

    ns = parser.parse_args()
    locals().update(ns.__dict__)
    remote, reponame = discover(repospec, verbose)
    if verbose and remote:
        print(f'remote = {remote}, reponame = {reponame}')
    if remote:
        print(
            clone(
                remote,
                reponame,
                revision,
                clonepath,
                mirrorpath,
                versioning=versioning))
    else:
        print(f"Failed to discover repository: {repospec}")

if __name__ == '__main__':
    main()

