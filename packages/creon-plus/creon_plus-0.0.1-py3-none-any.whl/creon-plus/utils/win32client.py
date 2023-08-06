from typing import TYPE_CHECKING
import win32com.client

if TYPE_CHECKING:
    from models import Module, EventHandler


def dispatch(name: str):
    return win32com.client.Dispatch(name)

def bind(module: 'Module', handler: 'EventHandler') -> 'EventHandler':
    return win32com.client.WithEvents(module, handler)