"""
Everything needed together for SpoolDB

With a little test program built in.

It contains the database and some functions
"""

from .spooldb import SpoolDB
from .dbfunc import open, openshelve

VERSION_INFO = (0, 1, 0)
VERSION = '.'.join(map(str, VERSION_INFO))
__version__ = VERSION

__author__ = "MXPSQL"

# Example program embedded
if __name__ == "__main__":
    with open('test.db', flag='c', format='json') as db:
        db["yes"] = "yes"
        db["high heel"] = "spool pumps"
        db["i"] = {
            "map": True,
            "list": [1, 2, 3],
            "tdb": {
                'ls': "true",
                "dir": True,
                "pax": True,
                "node": 'yes'
            }
        }
        db["lisp"] = ["common lisp", "scheme", "clojure"]

        for i in range(0, 5):
            db[i] = i