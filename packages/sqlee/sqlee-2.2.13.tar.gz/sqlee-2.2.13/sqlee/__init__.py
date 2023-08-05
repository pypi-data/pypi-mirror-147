from .sqlee import SqleeRepository
from .config import __version__
from .utils.exceptions import VersionError
from .utils.utils import typeassert

__name__ = "sqlee"
__version__ = __version__
__all__ = [
    'connect', 'utils',
    ]
__author__ = "Entropy <fu050409@163.com>"
__incantation__ = "嗡嘛呢叭咪吽"

@typeassert
def connect(name: str, user: str, token: str, *args, **kwargs):
    if "owner" in kwargs or "repo" in kwargs:
        raise VersionError("该数据库连接方式已在2.0.0版本后被弃用.")
    return SqleeRepository(access_token=token, repo=name, owner=user, *args, **kwargs)
