#!/usr/bin/env python

import sys
import glob
import os
import re
import subprocess

PYTHONS = ['2.7', '3.5', '3.6']

try:
    target_dir = sys.argv[1]
except KeyError:
    target_dir = os.getcwd()
target_dir = os.path.abspath(target_dir)

def _check(whl, python):
    arg = ['docker', 'run', '-t', '-v', '{}:/io'.format(target_dir),
           'pymor/python:{}'.format(python),
           'bash', '-c', 'pip install /io/{}'.format(whl)]
    return subprocess.check_call(arg)

py_regex = re.compile('(?:.*\-cp)(\d\d)(?:\-.*\.whl)')
for whl in glob.glob('{}/*whl'.format(target_dir)):
    whl = os.path.basename(whl)
    if '-win' in whl:
        print('Not checking Windows Wheel {}'.format(whl), file=sys.stderr)
        continue
    python = '{}.{}'.format(*py_regex.match(whl).group(1))
    if python not in PYTHONS:
        raise RuntimeError('cannot check {}, wrong python version {}'.format(whl, python))
    _check(whl, python)
