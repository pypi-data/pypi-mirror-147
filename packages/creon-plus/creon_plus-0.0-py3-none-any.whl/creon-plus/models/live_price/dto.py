from dataclasses import dataclass


@dataclass
class LivePrice:
    code: str
    name: str
    price: int
    time: int