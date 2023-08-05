#coding: utf-8
__author__ = "Entropy <fu050409@163.com>"

class URL:
    def __init__(self, url="https://gitee.com/"):
        self.url = url if url != None else self.url
        self.url = self.url if self.url[-1] == "/" else self.url + "/"
        
    def __add__(self, value):
        value = str(value)
        value = value if value[-1] == "/" else value + "/"
        return URL(url=self.url + value)
        
    def __truediv__(self, value):
        value = str(value)
        value = value if value[-1] == "/" else value + "/"
        return URL(url=self.url + value)

    def __str__(self):
        return self.url
