from typing import TYPE_CHECKING, Union, Any

from utils import dispatch
from models.creon import Module


class CreonAPI:
    __module: Union['Module', Any]

    def __init__(self, name: str) -> None:
        self.__module = Module(name)