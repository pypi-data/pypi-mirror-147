from inspect import signature
from functools import wraps
import typing

def typeassert(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not __debug__:
            return func

        bounds = signature(func).bind(*args, **kwargs).arguments.items()
        annotations = func.__annotations__
        for name, value in bounds:
            if name in annotations:
                if typing.get_origin(annotations[name]) == typing.Union:
                    if not issubclass(type(value), typing.get_args(annotations[name])):
                        attributes = ""
                        for attribute in typing.get_args(annotations[name]):
                            attributes += "%s 或 " % attribute.__name__
                        attributes = attributes[:-3]
                        raise TypeError(
                            '参数 {} 必须是类型 {}.'.format(name, attributes)
                            )
                    continue
                if not isinstance(value, annotations[name]):
                    raise TypeError(
                            '参数 {} 必须是类型 {}.'.format(name, annotations[name].__name__)
                            )
        result = func(*args, **kwargs)
        if not "return" in annotations:
            return result
        if typing.get_origin(annotations["return"]) == typing.Union:
            if not issubclass(type(result), typing.get_args(annotations["return"])):
                attributes = ""
                for attribute in typing.get_args(annotations["return"]):
                    attributes += "%s 或 " % attribute.__name__
                attributes = attributes[:-3]
                raise TypeError(
                    '返回的值必须是类型 %s.' % attributes
                    )
            return result
        if not isinstance(result, annotations["return"]):
            raise TypeError(
                    '返回的值必须是类型 %s.' % annotations["return"].__name__
                    )
        return result
    return wrapper