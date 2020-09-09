#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

sys.dont_write_bytecode = True

from ruamel import yaml
from pprint import pprint
from subprocess import Popen, PIPE, CalledProcessError
from contextlib import contextmanager
from argparse import ArgumentParser, RawDescriptionHelpFormatter

def expand(path):
    if path:
        return os.path.abspath(os.path.expanduser(path))

@contextmanager
def cd(*args, mkdir=True, verbose=False, **kwargs):
    path = os.path.sep.join(args)
    path = os.path.normpath(path)
    path = os.path.expanduser(path)
    prev = os.getcwd()
    if path != prev:
        if mkdir:
            call('mkdir -p '+path, verbose=verbose)
        os.chdir(path)
        curr = os.getcwd()
        sys.path.append(curr)
        if verbose:
            print('cd '+curr)
    try:
        yield
    finally:
        if path != prev:
            sys.path.remove(curr)
            os.chdir(prev)
            if verbose:
                print('cd '+prev)

def call(cmd, stdout=PIPE, stderr=PIPE, shell=True, nerf=False, throw=True, verbose=False):
    if verbose or nerf:
        print(cmd)
    if nerf:
        return (None, 'nerfed', 'nerfed')
    process = Popen(cmd, stdout=stdout, stderr=stderr, shell=shell)
    stdout, stderr = [stream.decode('utf-8') for stream in process.communicate()]
    exitcode = process.poll()
    if verbose:
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
    if throw and exitcode:
        message = f'cmd={cmd}; stdout={stdout}; stderr={stderr}'
        raise CalledProcessError(exitcode, message)
    return exitcode, stdout, stderr

def ls_remote(repourl, throw=True, verbose=False):
    return call('git ls-remote ' + repourl, throw=throw, verbose=verbose)

def clone(remote, reponame, revision, clonepath, mirrorpath, username=None, useremail=None, versioning=False):
    clonepath = expand(clonepath)
    mirrorpath = expand(mirrorpath)
    mirror = ''
    if mirrorpath:
        mirror = f'--reference {mirrorpath}/{reponame}.git'
    path = os.path.join(clonepath, reponame)
    repopath = reponame
    if versioning:
        repopath = os.path.join(repopath, revision)
    with cd(clonepath, mkdir=True):
        if not os.path.isdir(repopath):
            call(f'git clone {mirror} {remote}/{reponame} {repopath}')
        with cd(repopath):
            call('git clean -xfd')
            call('git checkout '+revision)
            if username and useremail:
                call(f'git config user.name "{username}"')
                call(f'git config user.email "{useremail}"')
    return os.path.join(clonepath, repopath)
