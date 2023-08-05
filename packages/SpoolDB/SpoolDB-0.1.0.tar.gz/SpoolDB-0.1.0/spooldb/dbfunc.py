"""
Utility and extra functions here
"""

import shelve
from .spooldb import SpoolDB

def open(filename=None, data={}, flag='c', mode=None, format='pickle', *args, **kwargs):
    """
    Open a SpoolDB.
    """
    return SpoolDB(filename, data=data, flag=flag, mode=mode, format=format, *args, **kwargs)

def openshelve(filename=None, data={}, flag='c', mode=None, format='pickle', *args, **kwargs):
    """
    Open a shelve instance with SpoolDB as the backend.
    """
    return shelve.Shelf(SpoolDB(filename, data=data, flag=flag, mode=mode, format=format, *args, **kwargs))