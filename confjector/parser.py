from typing import Any, Type, TypeVar

from pydantic import BaseSettings
import yaml


BaseSettingsType = TypeVar('BaseSettingsType', bound='BaseSettings')


def parse(conf_cls: Type[BaseSettingsType], conf_path: str) -> BaseSettingsType:
    """
    Parses provided file, instantiates and returns provided config class with parsed data.
    If config file has section with the same name as the config class, returns only that section/
    Returns everything from the config otherwise.
    :param conf_cls: Type[BaseSettings], class into which config should be parsed.
    :param conf_path: path to a file to be parsed.
    :return: BaseSettings, instantiated and parsed config object.
    """
    config_dict = _parse_file_to_dict(conf_path)

    # Try to find concrete settings
    section = config_dict.get(conf_cls.__name__.lower())
    if section is not None:
        return conf_cls(**section)

    # Whole config file will be put into the config class
    return conf_cls(**config_dict)


def _parse_file_to_dict(conf_path: str) -> dict[str, Any]:
    with open(conf_path, "r") as stream:
        return yaml.safe_load(stream)
