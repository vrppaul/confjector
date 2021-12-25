from typing import Callable, ParamSpec, Concatenate, TypeVar, get_type_hints, Type

from pydantic import BaseSettings

from .parser import parse

P = ParamSpec("P")
R = TypeVar("R")
OriginalFunc = Callable[Concatenate[BaseSettings, P], R]
DecoratedFunc = Callable[P, R]


def inject(*, conf_path: str) -> Callable[[OriginalFunc], DecoratedFunc]:
    """
    Parses a configuration file, provided by path and injects into the decorated function.

    :param conf_path: str, path to a config file.
    """
    def wrapper(func: OriginalFunc) -> DecoratedFunc:
        def inner(*args: P.args, **kwargs: P.kwargs) -> R:
            conf_cls = _get_settings_model(func)
            if not conf_cls:
                raise ValueError(
                    "No correct conf class is provided in arguments. "
                    "Please provide a subclass of pydantic.BaseSettings "
                    "for decorator to work properly."
                )
            parsed_config = parse(conf_cls=conf_cls, conf_path=conf_path)
            return func(parsed_config, *args, **kwargs)
        return inner
    return wrapper


def _get_settings_model(func: OriginalFunc) -> Type[BaseSettings] | None:
    """
    Gets a type of configuration, which should be injected later.
    """
    arg_types = get_type_hints(func)
    arg_types.pop("return")
    for arg_type in arg_types.values():
        if issubclass(arg_type, BaseSettings):
            return arg_type
    return None

