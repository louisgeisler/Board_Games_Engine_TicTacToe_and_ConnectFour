"""
File: utils/FilesUtils.py
File Created: 16/07/2022
Authors: Louis Geisler, Emile Duquennoy
"""

import inspect
import sys


def get_list_imported_classes(_class):
    # A list of tuples [(<class name>, <class>), ...]
    members = inspect.getmembers(sys.modules[_class.__name__], inspect.isclass)

    # We return a list of classes only
    return list(map(lambda x: x[1], members))
