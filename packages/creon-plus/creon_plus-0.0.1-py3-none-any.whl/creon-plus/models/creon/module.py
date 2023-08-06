from typing import Any, Union

from utils.win32client import dispatch


class Module:
    __module: Any

    def __init__(self, name: str) -> None:
        self.__module = dispatch(name)

    def get_header_value(self, type: int) -> Union[int, str, float]:
        return self.__module.GetHeaderValue(type)

    def set_input_value(self, type: int, code: str):
        self.__module.SetInputValue(type, code)

    def subscribe(self):
        self.__module.Subscribe()

    def unsubscribe(self):
        self.__module.Unsubscribe()