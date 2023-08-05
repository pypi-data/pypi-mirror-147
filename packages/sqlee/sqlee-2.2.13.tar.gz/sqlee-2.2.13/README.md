# Sqlee
由中国左旋联盟开阳信息序列开发的基于Gitee API搭建的数据存储系统.

## 安装
你可以通过命令`pip install sqlee`或`python -m pip install sqlee`来安装Sqlee数据库.

### Sqlee目录树
```
├─utils
│  │  backend.py
│  │  crypto.py
│  │  exceptions.py
│  │  gitee.py
│  │  urlparse.py
│  │  __init__.py
│  │
│  └─django
│        handler.py
│        models.py
│        verify.py
│        __init__.py
├─sqlee.py
└─__init__.py
```

## 基本使用

### 创建新的Sqlee数据库
```python
from sqlee.utils import gitee
gitee.make_repo(name="数据库名", token="Gitee API Token", user="Gitee用户名")
```

### 连接已有的Sqlee数据库
你可以使用以下代码来创建一个新的数据库实例：
```python
import sqlee

db = sqlee.connect(
        access_token = "你的Gitee API Token",
        user = "你的Gitee用户名",
        name = "你的数据库名",
    )

```

### 创建表
```python
db.objects.create(name="表名", namespace=["索引", "命名域1", "命名域2"])
```

### 删除表
```python
db.objects.delete(name="表名")
```

### 读取表
```python
db.objects.all() #读取所有表(同时捕获所有数据)
db.objects.get(name="实例表名") #读取指定数据表(同时捕获该表所有数据)
db.objects.get(name="实例表名", directly_load=False) #读取指定数据表(但不捕获该表所有数据)
```

### 数据的读取与筛选
```python
table = db.objects.get(name="Table")
table.objects.all() #读取全部的数据
table.objects.create(index=0, name1=1, name2=2) #创建新的数据
table.objects.get(index=0) #读取索引为 int 0 的数据(如果筛选出了多个数据，它将抛出异常)
table.objects.get(index=0).delete() #删除索引为 int 0 的数据
table.objects.filter(name1=1) #筛选命名域 name1 值为 int 1 的数据栏
```
Sqlee和其它的数据库不同，它并不强制你在同一栏的同一命名域中使用同样类型的数据，同时，任何数据对于Sqlee来说都是可被存储的。同时，Sqlee和其它的数据库不同，它的索引并不一定为`int id`，它同样可以是`str index`，当然，你同样可以将命名域的第一位设置为`id`，但是在创建新的数据栏时，你不必传入栏`id`的数据，否则它将抛出`ValueError`的异常.
值得注意的是，如果你采用索引来读取和筛选数据，它将提供一个更加迅捷的查询.

### 命令行
`db.interact()`

## 版权
Copyright © 2011-2021 中国左旋联盟 All Rights Reserved.