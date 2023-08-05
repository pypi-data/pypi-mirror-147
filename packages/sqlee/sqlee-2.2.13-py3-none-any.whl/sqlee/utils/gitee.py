#coding: utf-8
"""
   作者: Entropy
   版本: 1.0
"""
from urllib.parse import urlencode
from typing import Union

import requests
import json
import base64

if __name__ == "__main__":
    from exceptions import (RepositoryNotFoundError, RepositoryConnectionRefusedError,
                            InternetError, ColumnNotFoundError, RepositoryNotFound)
    from utils import typeassert
    from urlparse import URL
else:
    from .exceptions import (RepositoryNotFoundError, RepositoryConnectionRefusedError,
                             InternetError, ColumnNotFoundError, RepositoryNotFound)
    from .utils import typeassert
    from .urlparse import URL

class GiteeRepo:
    token: str
    user: str
    repo: str
    def __init__(self, token: str, user: str, repo: str):
        self.token = token
        self.user = user
        self.repo = repo
        self.url = "https://gitee.com/" + user + "/" + repo + "/"

        try:
            exists = self.has_repo(name=repo, user=user, token=token)
            if not exists:
                raise RepositoryNotFoundError(self.repo)
        except requests.RequestException:
            raise InternetError()

        self.types = {}
        self.types["int"] = int
        self.types["str"] = str

    @staticmethod
    @typeassert
    def has_repo(name: str, user: str, token: str):
        query = requests.get(
                url = "https://gitee.com/api/v5/user/repos",
                data = {"access_token": token}
                )
        if query.status_code // 100 != 2:
            raise RepositoryConnectionRefusedError(self.repo, status_code=status_code)
        all_repos = query.json()
        exists = False
        for repos in all_repos:
            if name == repos["name"] and user == repos["owner"]["login"]:
                exists = True
        return exists

    @typeassert
    def get_file(self, path: Union[str, URL]):
        query = requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text
        if query == "[]":
            raise ColumnNotFoundError(path)
        return base64.b64decode(json.loads(query)["content"].encode()).decode()

    @typeassert
    def get_data(self, path: Union[str, URL]):
        return json.loads(base64.b64decode(json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)["content"].encode()).decode())["content"]

    @typeassert
    def list_file(self, path: Union[str, URL], detail: bool=False, int: bool=False, dir: bool=False):
        if detail and int:
            print("[-] 参数'detail'与参数'int'不可以均设置为True.")
            return False
        result = []
        reception = json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)
        for file in reception:
            if detail:
                if not dir:
                    if file["type"] != "dir":
                        result.append(file)
                else:
                    result.append(file)
                continue
                
            if not int:
                if not dir:
                    if file["type"] != "dir" and file["name"] != ".keep" and file["name"] != ".namespace":
                        result.append(file["name"])
                else:
                    if file["name"] != ".keep" and file["name"] != ".namespace":
                        result.append(file["name"])
            else:
                if file["name"] != ".keep" and file["name"] != ".namespace":
                    if not dir:
                        if file["type"] != "dir":
                            try:
                                result.append(self.types["int"](file["name"]))
                            except ValueError:
                                raise ValueError("目标文件名不支持转换为数字.")
                    else:
                        try:
                            result.append(self.types["int"](file["name"]))
                        except ValueError:
                            raise ValueError("目标文件名不支持转换为数字.")
        return tuple(result)

    @typeassert
    def list_file_int(self, path: Union[str, URL]):
        return self.list_file(path=path, detail=False, int=True, dir=False)

    @typeassert
    def list_folder(self, path: Union[str, URL], detail: bool=False, int: bool=False):
        if detail and int:
            print("[-] 参数'detail'与参数'int'不可以均设置为True.")
            return False
        result = []
        reception = json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)
        for file in reception:
            if detail:
                if file["type"] == "dir":
                    result.append(file)
                continue

            if file["type"] == "dir":
                if not int:
                    result.append(file["name"])
                else:
                    try:
                        result.append(self.types["int"](file["name"]))
                    except ValueError:
                        raise ValueError("目标文件夹名不支持转换为数字.")
        return tuple(result)

    @typeassert
    def list_dir(self, path: Union[str, URL], detail: bool=False, int: bool=False):
        return self.list_folder(path=path, detail=detail, int=int)

    @typeassert
    def list_folder_int(self, path: Union[str, URL]):
        result = []
        reception = json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)
        for file in reception:
            if file["type"] == "dir":
                result.append(self.types["int"](file["name"]))
        return tuple(result)

    @typeassert
    def upload_file(self, path: Union[str, URL], content: str):
        return requests.post(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}",
            data = {
                "access_token": self.token,
                "content": base64.b64encode(content.encode()),
                "message": "UPLOAD FILE - SQLEE"
                }
            )

    @typeassert
    def update_file(self, path: Union[str, URL], content: str):
        return requests.put(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}",
            data = {
                "access_token": self.token,
                "content": base64.b64encode(content.encode()),
                "sha": self.get_sha(path=path),
                "message": "UPDATE FILE - SQLEE"
                }
            )

    @typeassert
    def delete_file(self, path: Union[str, URL]):
        data = {
            "access_token": self.token,
            "sha": self.get_sha(path=path),
            "message": "DELETE FILE - SQLEE"
            }
        return requests.delete(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?" + urlencode(data)
            )

    @typeassert
    def get_sha(self, path: Union[str, URL]):
        result = json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)
        if isinstance(result, dict):
            if "sha" in result:
                return result["sha"]
            else:
                raise ValueError("捕获到的数据无法提取文件sha值.")
        else:
            print(result)
            raise ValueError("捕获到的数据无法提取文件sha值.")

    @typeassert
    def make_folder(self, path: Union[str, URL]):
        return requests.post(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}/.keep",
            data = {
                "access_token": self.token,
                "content": base64.b64encode("*".encode()),
                "message": "MAKE FOLDER - SQLEE"
                }
            )

    @typeassert
    def drop_folder(self, path: Union[str, URL]):
        for folder in self.list_file(path=path, detail=True, dir=True):
            if folder["type"] == "dir":
                self.drop_folder(path=folder["path"])
            elif folder["type"] == "file":
                self.delete_file(path=folder["path"])
        return True
        
    def __str__(self):
        return self.repo

@typeassert
def make_repo(token: str, user: str, name: str, private: bool=True, auto_init: bool=True):
    if not token or not user or not name:
        raise ValueError("参数不全.")
    if GiteeRepo.has_repo(name=name, user=user, token=token):
        print("仓库 %s 已存在." % name)
        return
    else:
        print(RepositoryNotFound(name))
    return requests.post(
        url = "https://gitee.com/api/v5/user/repos",
        data = {
            'name': name,
            'access_token': token,
            'auto_init': auto_init,
            'private': private,
        }
    )