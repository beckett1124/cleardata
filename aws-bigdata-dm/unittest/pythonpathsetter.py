#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T11:11:25+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T11:15:13+08:00
import sys
import fnmatch
from os.path import abspath, dirname

AMBLEDIR = dirname(abspath(__file__))


def add_path(path, end=False):
    if not end:
        remove_path(path)
        sys.path.insert(0, path)
    elif not any(fnmatch.fnmatch(p, path) for p in sys.path):
        sys.path.append(path)


def remove_path(path):
    sys.path = [p for p in sys.path if not fnmatch.fnmatch(p, path)]


add_path(dirname(AMBLEDIR))
remove_path(AMBLEDIR)
