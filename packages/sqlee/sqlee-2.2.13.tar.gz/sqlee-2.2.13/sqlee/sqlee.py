#coding: utf-8

import os, sys, json
import requests, traceback
import argparse, shlex, platform
import importlib

from prompt_toolkit import prompt
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
from requests import get, post, put, delete
from typing import Union

if __name__ == "__main__":
    from utils import gitee
    from utils.backend import SqleeColumn, SqleeTable
    from utils.exceptions import RepositoryNotFoundError, TableNotFoundError, RepositoryNotFound
    from utils.urlparse import URL
    from utils.crypto import CryptoHandler
    from utils.utils import typeassert
    from config import __version__
else:
    from .utils import gitee
    from .utils.backend import SqleeColumn, SqleeTable
    from .utils.exceptions import RepositoryNotFoundError, TableNotFoundError, RepositoryNotFound
    from .utils.urlparse import URL
    from .utils.crypto import CryptoHandler
    from .utils.utils import typeassert
    from .config import __version__

class termios:
    class error(RuntimeError):
        pass
Windows = True if platform.system() == "Windows" else False

class objects:
    def __init__(self, obj=None):
        self.obj = obj

    def all(self):
        return self.obj.all_tables()
    
    @typeassert
    def get(self, name: str, directly_load: bool=True):
        if name in self.obj.repo.list_folder(path=""):
            return SqleeTable(name=name, repo=self.obj.repo, directly_load=directly_load)
        raise TableNotFoundError(name)

    @typeassert
    def create(self, name: str, namespace: Union[list, tuple]):
        return self.obj.create_table(name=name, namespace=namespace)

    @typeassert
    def delete(self, name: str):
        return self.obj.drop_table(name)
    
    def count(self):
        return len(self.obj.repo.list_folder(path="", detail=True))

    @property
    def length(self):
        return len(self.obj.repo.list_folder(path="", detail=True))

class SqleeRepository:
    access_token: str
    repo: str
    owner: str
    def __init__(self, access_token, repo, owner, auto_make: bool=False):
        self.access_token = access_token
        if auto_make:
            gitee.make_repo(name=repo, user=owner, token=access_token)
        self.repo = gitee.GiteeRepo(token=access_token, user=owner, repo=repo)
        self.owner = owner
        self.objects = objects(obj=self)

    def all_tables(self):
        datas = self.repo.list_folder(path="", detail=True)
        tables = [SqleeTable(name=data['name'], repo=self.repo) for data in datas if data['type'] == 'dir']
        return tables

    @typeassert
    def create_table(self, name: str, namespace: Union[list, tuple]):
        if not namespace or not name:
            raise ValueError("未提供足够的参数.")
        for value in ["data", "length", "update", "delete",
                      "namespace", "count", "sync", "repo"]:
            if value in namespace:
                raise ValueError("命名域不可以被命名为: %s." % value)
        make = self.repo.make_folder(path=name)
        self.repo.upload_file(path=URL(name)/".namespace", content=json.dumps(namespace))
        return make

    @typeassert
    def drop_table(self, name: str):
        return self.repo.drop_folder(path=name)

    @typeassert
    def clear(self, sure: bool=False):
        if not sure:
            confirm = input("你确定删除本数据库(同时删除云端数据)吗? (Y/N) ")
            if confirm == "Y" or confirm == "y":
                pass
            else:
                print("忽略.")
                return
        url = f"https://gitee.com/api/v5/repos/{self.owner}/{self.repo}"

        requests.delete(
            url = url,
            data = {"access_token": self.access_token}
        )
        return True
    
    def interact(self):
        def hotreload():
            import os, sys
            os.system("python %s" % sys.argv[0])

        print("SQLEE %s\nCopyright © 中国左旋联盟 × Freet安全组" % (__version__))
        all_tables = self.all_tables
        get_all_tables = self.all_tables
        tables = self.all_tables
        create_table = self.create_table
        create = self.create_table
        while True:
            try:
                cmd = prompt('SQLEE>>> ')
                if cmd.replace(" ", "") == "exit()":
                    return
            except NoConsoleScreenBufferError:
                if Windows:
                    print("SQLEE CONSOLE必须在 'cmd.exe' 中运行 !")
                    restart = input("是否要在CMD中重新执行本程序(或脚本)? (Y/N) ")
                    restart = True if restart == "Y" else False
                    if restart:
                        os.system("python %s" % sys.argv[0])
                else:
                    print("你的终端暂不支持运行HFCONSOLE.")
                exit()
            except termios.error:
                print('[-] Termios 错误, 你的终端不支持SQLEE CONSOLE或由于SQLEE CONSOLE开启时终端显示大小被调整, 请检查终端设置并重试.')
                exit()
            except KeyboardInterrupt:
                print("执行 'exit()' 来退出该会话.")
                continue
            except EOFError:
                print("不要使用 'Ctrl+D'(EOF) 来退出, 用 'exit()' 来代替它.")
                continue

            try:
                exec(cmd)
            except:
                traceback.print_exc()