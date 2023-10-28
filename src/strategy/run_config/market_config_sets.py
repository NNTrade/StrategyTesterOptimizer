from __future__ import annotations
from typing import MutableMapping, Tuple, Dict, List
from datetime import date
from .market_config import MarketConfig


class MarketConfigSets:
    class Builder:
        def __init__(self) -> None:
            self.data: List[MarketConfig] = []
            pass

        def add_stocks(self, stocks: List[str], from_dt: date, untill_dt: date) -> MarketConfigSets.Builder:
            self.data.append(MarketConfig(stocks.copy(), from_dt, untill_dt))
            return self

        def add_stock(self, stock: str, from_dt: date, untill_dt: date) -> MarketConfigSets.Builder:
            self.data.append(MarketConfig([stock], from_dt, untill_dt))
            return self

        def add_stocks_set(self, stocks_set: List[List[str]], from_dt: date, untill_dt: date) -> MarketConfigSets.Builder:
            for stocks in stocks_set:
                if isinstance(stocks, str):
                    raise AttributeError("Stocks set must contain list of stocks set.",name="stocks_set")
                self.data.append(MarketConfig(stocks.copy(), from_dt, untill_dt))
            return self

        def build(self) -> MarketConfigSets:
            return MarketConfigSets(self.data)

    def __init__(self, data: List[MarketConfig] = []):
        if len(data) == 0:
            raise AttributeError("Cann't set no market configs")
        self.__data: Tuple = tuple(data)

    def as_records(self) -> List[MarketConfig]:
        return [rec for rec in self.__data]
