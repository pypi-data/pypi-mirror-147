#coding: utf-8
from sqlee.utils.django import models
from django.forms.models import model_to_dict
from threading import Thread

import argparse
import os
import sqlee
import sys
import json
import requests

if __name__ == "__main__":
    from verify import verify_django
else:
    from .verify import verify_django

def init():
    url = json.loads(requests.get("https://gitee.com/api/v5/repos/{user}/{name}?access_token={token}".format(
        user = settings.SQLEE_SETTINGS["OWNER"],
        name = settings.SQLEE_SETTINGS["NAME"],
        token = settings.SQLEE_SETTINGS["TOKEN"]
        )).text)
    if "message" in url:
        if url["message"] == "Not Found Project":
            print("开始创建数据库...")
            sqlee.utils.gitee.make_repo(token=settings.SQLEE_SETTINGS["TOKEN"], user=settings.SQLEE_SETTINGS["OWNER"], name=settings.SQLEE_SETTINGS["NAME"]).text
        else:
            raise Exception(url["message"])
    else:
        return True
            
def migrate():
    repo = sqlee.connect(token=settings.SQLEE_SETTINGS["TOKEN"], repo=settings.SQLEE_SETTINGS["NAME"], owner=settings.SQLEE_SETTINGS["OWNER"])
    sys.path.append(settings.BASE_DIR)

    for app in settings.INSTALLED_APPS:
        try:
            print("正在解析模块'%s'内的SQLEE数据库声明文件." % (app))
            sqlee_models = __import__("%s.sqlee_models" % (app)).sqlee_models
        except ModuleNotFoundError:
            print("模块'%s'中未找到SQLEE数据库声明文件." % (app))
            continue
        for model in dir(sqlee_models):
            model = getattr(sqlee_models, model)
            if hasattr(model, "repo"):
                print("正在读取Model '%s'" % (model.__class__.__name__))
                print("\n正在创建数据表: '%s'\n" % (model.tablename))
                repo.objects.create(name=model.tablename, namespace=model.namespaces)
    return True

class SYNC_DB(Thread):
    def __init__(self, repo=None, data=None, tablename=None):
        Thread.__init__(self)
        self.repo = repo
        self.data = data
        self.tablename = tablename

    def run(self):
        self.repo.objects.get(name=self.tablename).objects.create(**self.data)

def format_sql_data(sql_data):
    for data in sql_data:
        sql_data[data] = str(sql_data[data])
    return sql_data

def sync():
    from django.db import models
    repo = sqlee.connect(token=settings.SQLEE_SETTINGS["TOKEN"], repo=settings.SQLEE_SETTINGS["NAME"], owner=settings.SQLEE_SETTINGS["OWNER"])
    sys.path.append(settings.BASE_DIR)

    for app in settings.INSTALLED_APPS:
        try:
            print("正在解析模块'%s'内的DJANGO数据库声明文件." % (app))
            django_models = __import__("%s.models" % (app)).models
            sqlee_models = __import__("%s.sqlee_models" % (app)).sqlee_models
        except ModuleNotFoundError:
            print("模块'%s'中未找到DJANGO数据库声明文件." % (app))
            continue
        except AttributeError:
            print("模块'%s'中未找到DJANGO数据库声明文件." % (app))
            continue

        datas = []
        for model in dir(django_models):
            if not hasattr(eval("sqlee_models"), model) and not hasattr(eval("django_models"), model):
                continue
            sqlee_model = getattr(eval("sqlee_models"), model)
            model = getattr(eval("django_models"), model)

            if hasattr(model, "__base__"):
                print("正在读取Model '%s'" % (model.__name__))
                if model.__base__ is models.Model:
                    print("\n正在读取数据表: '%s'\n" % (sqlee_model().tablename))
                    sql_datas = model.objects.all()
                    for data in sql_datas:
                        datas.append(format_sql_data(model_to_dict(data)))
                        ### USES THREAD ###
                        #print(format_sql_data(model_to_dict(data)))
                        #sync = SYNC_DB(repo=repo, tablename=sqlee_model().tablename, data=format_sql_data(model_to_dict(data)))
                        #sync.setDaemon(True)
                        #sync.start()
                        ### USES THREAD ###
                        repo.objects.get(name=sqlee_model().tablename).objects.create(**format_sql_data(model_to_dict(data)))
                    #pool = SYNC_DB_POOL(repo=repo, datas=format_sql_data(model_to_dict(sql_datas)), tablename=sqlee_model().tablename)
                    #pool.setDaemon(True)
    return datas

def execute_from_command_line(argv):
    return eval(argv[1])()

settings = verify_django()
