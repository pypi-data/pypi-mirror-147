#coding: utf-8

from sqlee.utils.backend import SqleeTable
from sqlee.utils.backend import table_objects

import os
import json
import requests

if __name__ == "__main__":
    from verify import verify_django
else:
    from .verify import verify_django

class Model:
    def __init__(self):
        self.repo = settings.SQLEE.repo
        self.tablename = "%s_%s" % (
            self.app,
            self.__class__.__name__
            )
        try:
            self.table = SqleeTable(name=self.tablename, repo=self.repo)
            self.objects = table_objects(obj=self.table)
        except Exception:
            pass

settings = verify_django()
