#coding: utf-8
if __name__ == "__main__":
    from gitee import GiteeRepo
    from urlparse import URL
    from crypto import CryptoHandler
    from exceptions import (ColumnDataDoesNotFit, ColumnNotFoundError, 
                           DataWasNotGiven, DataWasNotGivenError)
    from utils import typeassert
else:
    from .gitee import GiteeRepo
    from .urlparse import URL
    from .crypto import CryptoHandler
    from .exceptions import (ColumnDataDoesNotFit, ColumnNotFoundError,
                            DataWasNotGiven, DataWasNotGivenError)
    from .utils import typeassert

import json, warnings
from typing import Union

@typeassert
def model_to_data(model: Union[list, tuple]):
    return tuple([i.data if hasattr(i, "data") else i for i in model])

class table_objects:
    def __init__(self, obj=None):
        self.obj = obj

    def all(self):
        """ Usage: all() """
        if not self.obj._loaded: self.obj.sync()
        return self.obj.columns
    
    def get(self, *args, **kwargs):
        """ Usage: get(**namespace) """
        if len(kwargs) == 1 and self.obj.index in kwargs:
            return SqleeColumn(
                    path = URL(self.obj.name) / kwargs[self.obj.index],
                    repo = self.obj.repo,
                    index = self.obj.index,
                    table = self.obj,
                    index_data = kwargs[self.obj.index],
                    namespace = self.obj.namespace,
                    )
        if not self.obj._loaded: self.obj.sync()
        need = len(kwargs)
        result = []
        for column in self.obj.columns:
            transit = 0
            for kwarg in kwargs:
                if kwargs[kwarg] == getattr(column, kwarg):
                    transit += 1
            if transit == need:
                result.append(column)
        if len(result) != 1:
            raise ValueError("找到了 %d 个匹配的数据，如果你试图筛选多数据，请参考‘filter’." % len(result))
        return result[0]

    def create(self, *args, **kwargs):
        """ Usage: create(**namespace) """
        if self.obj.index == "id":
            if "id" in kwargs:
                raise ValueError("索引为 id 的表不应当将 id 作为数据参数传入.")
        else:
            if not self.obj.index in kwargs:
                raise DataWasNotGivenError(namespace=self.obj.index)

        column = self._get_cloumn(kwargs)

        all_columns = self.obj.repo.list_file(self.obj.name)
        if str(column) in all_columns:
            raise ValueError("目标索引已存在.")

        datas = []
        for namespace in self.obj.namespace:
            if namespace == self.obj.index:
                continue
            if namespace in kwargs:
                datas.append(kwargs[namespace])
            else:
                print(DataWasNotGiven(namespace=namespace))
                datas.append(None)

        self.obj.repo.upload_file(
            path = URL(self.obj.name) / column,
            content = self.obj.crypto.encrypt_to_str(json.dumps(datas))
            )

        new_column = SqleeColumn(
                            path = URL(self.obj.name) / column,
                            repo = self.obj.repo,
                            index = self.obj.index,
                            index_data = column,
                            table = self.obj,
                            namespace = self.obj.namespace,
                            )
        self.obj.columns = list(self.obj.columns)
        self.obj.columns.append(new_column)
        return new_column

    def delete(self, *args, **kwargs):
        """ Usage: delete(**namespace) """
        force_del = kwargs["force_del"] if "force_del" in kwargs else False
        if "*" in args:
            if force_del:
                return self.obj.delete_all()
            else:
                raise ValueError("您选择了清空Table，然而却没有下定决心，略过.")
        if len(kwargs) == 1 and self.obj.index in kwargs:
            return self.obj.repo.delete_file(path = URL(self.obj.name) / kwargs[self.obj.index])
        if not self.obj._loaded: self.obj.sync()
        need = len(kwargs)
        result = []
        for column in self.obj.columns:
            transit = 0
            for kwarg in kwargs:
                if kwargs[kwarg] == getattr(column, kwarg):
                    transit += 1
            if transit == need:
                result.append(column)
        if len(result) != 1 and not force_del:
            raise ValueError("找到了 %d 个匹配的数据，取消操作. 如果尝试删除多个数据，请加入参数force_del = True." % len(result))
        else:
            for column in result:
                self.obj.repo.delete_file(path = URL(self.obj.name) / column.index_data)
        return result[0]

        return self.obj.delete()
    
    @property
    def length(self):
        """ Usage: length """
        return len(self.obj.columns)

    def count(self):
        """ Usage: count() """
        return len(self.obj.columns)
    
    def filter(self, *args, **kwargs):
        """ Usage: filter(**namespace) """
        if len(kwargs) == 1 and self.obj.index in kwargs:
            if not kwargs[self.obj.index] in self.obj.repo.list_file_int(path=self.obj.index):
                print(ColumnNotFoundError(URL(self.obj.name) / kwargs[self.obj.index]))
                return []
            return [SqleeColumn(
                    path = URL(self.obj.name) / kwargs[self.obj.index],
                    repo = self.obj.repo,
                    index = self.obj.index,
                    table = self.obj,
                    index_data = kwargs[self.obj.index],
                    namespace = self.obj.namespace,
                    )]
        if not self.obj._loaded: self.obj.sync()
        need = len(kwargs)
        result = []
        for column in self.obj.columns:
            transit = 0
            for kwarg in kwargs:
                if kwargs[kwarg] == getattr(column, kwarg):
                    transit += 1
            if transit == need:
                result.append(column)
        return result

    def _get_cloumn(self, kwargs):
        if self.obj.index == "id":
            column = self.obj.repo.list_file_int(path=self.obj.name)
            if len(column) == 0:
                column = 0
            else:
                column = max(column) + 1
            return column
        else:
            if self.obj.index in kwargs:
                return kwargs[self.obj.index]
            else:
                raise ValueError("未传入索引数据 %s." % self.obj.index)

    def sync(self):
        """ Usage: sync() """
        return self.obj.sync()

class SqleeColumn:
    datas = []
    def __init__(self, path=None, repo=None, index=None, index_data=None, 
                 table=None, namespace=[], *args, **kwargs):
        if not isinstance(repo, GiteeRepo):
            raise ValueError("参数'repo'必须是GiteeRepo.")

        self.index = index
        self.index_data = index_data
        self.repo = repo
        self.table = table
        self.path = path
        self.namespace = namespace
        self.sync()

    @property
    def data(self):
        """ Usage: data """
        return model_to_data(self.datas)

    @property
    def length(self):
        """ Usage: length """
        return len(self.data)

    def count(self):
        """ Usage: count() """
        return len(self.data)

    def sync(self):
        """ Usage: sync() """
        self.datas = [self.index_data, ]

        self.datas += json.loads(self.table.crypto.decrypt_by_str(
            self.repo.get_file(path=self.path)
            ))

        i = 0
        for data in self.datas:
            setattr(self, self.namespace[i], data)
            i += 1

        if len(self.datas) != len(self.namespace):
            print(ColumnDataDoesNotFit(namespace=self.namespace, datas=self.datas))
        return self.datas

    def update(self, *args, **kwargs):
        """ Usage: update(**namespace) """
        for kwarg in kwargs:
            self.datas[self.namespace.index(kwarg)] = kwargs[kwarg]
        self.repo.update_file(
            path = self.path,
            content = self.table.crypto.encrypt_to_str(json.dumps(self.datas[1:]))
            )
        return self.sync()

    def delete(self):
        """ Usage: delete() """
        self.repo.delete_file(path = self.path)
        self.table.columns.remove(self)
        return True

class SqleeTable:
    columns = []
    _loaded = False
    def __init__(self, name=None, repo=None, directly_load=True, encrypt=True):
        if not isinstance(name, str) and not isinstance(name, URL):
            raise ValueError("参数 'name' 必须是字符串或URL.")
        if not isinstance(repo, GiteeRepo):
            raise ValueError("参数 'repo' 必须是GiteeRepo.")

        self.crypto = CryptoHandler(crypto=encrypt)
        self.name = name
        self.repo = repo
        self.namespace = json.loads(self.repo.get_file(path=URL(self.name)/".namespace"))
        self.index = self.namespace[0]
        self.url = URL()/self.repo.user/self.repo.repo/self.name
        self.objects = table_objects(obj=self)
        if directly_load:
            self.sync()
    
    def get_column(self, id=None):
        for column in self.columns:
            if column.id == id:
                return column
        else:
            raise ColumnNotFoundError(id)

    def insert(self, *args, **kwargs):
        return self.objects.create(*args, **kwargs)

    def sync(self):
        self.columns = []
        all_columns = self.repo.list_file_int(path=self.name) if self.index == "id" else self.repo.list_file(path=self.name)
        for column in all_columns:
            self.columns.append(
                SqleeColumn(
                    path = URL(self.name) / column,
                    repo = self.repo,
                    index = self.index,
                    index_data = column,
                    table = self,
                    namespace = self.namespace,
                    )
                )
        self._loaded = True
        return self.columns

    def delete_all(self):
        answer = self.repo.drop_folder(path=self.name)
        del self
        return answer