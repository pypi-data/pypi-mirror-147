from typing import TYPE_CHECKING
from models import EventHandler

if TYPE_CHECKING:
    from models import Module
    from models.live_price import LivePrice

class LivePriceHandler(EventHandler):
    def init(self, module: 'Module', dto: 'LivePrice') -> None:
        self.__module = module
        self.__dto = dto

    def subscribe(self) -> None:
        self.__module.subscribe()

    def OnReceived(self):
        self.__dto.code  = self.__module.get_header_value(0)
        self.__dto.name  = self.__module.get_header_value(1)
        self.__dto.price = self.__module.get_header_value(13)
        self.__dto.time  = self.__module.get_header_value(18)