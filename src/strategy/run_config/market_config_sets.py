from __future__ import annotations
from typing import MutableMapping, Tuple, Dict, List
from datetime import date
from .market_config import MarketConfig


class MarketConfigSets(MutableMapping):
    class Builder:
        def __init__(self) -> None:
            self.data = []
            pass

        def add_stocks(self, stocks: List[str], from_dt: date, untill_dt: date) -> MarketConfigSets.Builder:
            self.data.append(tuple(*stocks), from_dt, untill_dt)
            return self

        def add_stock(self, stock: str, from_dt: date, untill_dt: date) -> MarketConfigSets.Builder:
            self.data.append(tuple(stock), from_dt, untill_dt)
            return self

        def build(self) -> Tuple[Tuple[str], date, date]:
            return [(k, v[0], v[1]) for k, v in self.data.items()]

    def __init__(self, data=[]):
        if len(data) == 0:
            raise AttributeError("Cann't set no market configs")
        self.__data: Dict = data

    def as_records(self) -> List[MarketConfig]:
        return [(k, v[0], v[1]) for k, v in self.__data.items()]
