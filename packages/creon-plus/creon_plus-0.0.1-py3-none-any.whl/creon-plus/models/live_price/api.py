import json

from constants import STOCK_CUR
from models.live_price import LivePrice, LivePriceHandler
from models.creon import CreonAPI
from utils import bind


class LivePriceAPI(CreonAPI):
    __handler: LivePriceHandler
    def __init__(self, code: str) -> None:
        super().__init__(STOCK_CUR)
        self.__module.set_input_value(0, code)
        self.dto = LivePrice(code=code, name='', price=0, time=0)

    @property
    def message(self) -> str:
        """json message from dto"""
        return json.dumps(self.dto.__dict__, ensure_ascii=False)

    def subscribe(self):
        self.__handler = bind(self.__module, LivePriceHandler)
        self.__handler.init(self.__module, self.dto)
        self.__handler.subscribe()

    async def unsubscribe(self):
        self.__module.unsubscribe()
