from __future__ import annotations
from typing import MutableMapping, Tuple, Dict, List
from datetime import date
from .market_config import MarketConfig
from NNTrade.common import TimeFrame
from .stock_config import StockConfig

class MarketConfigSet:
    class Builder:
        def __init__(self) -> None:
            self.data: List[MarketConfig] = []
            pass

        def add_stocks(self, stocks: List[str], step_timeframe: TimeFrame, from_dt: date, untill_dt: date, aggregation_timeframe: TimeFrame = None) -> MarketConfigSet.Builder:
            for s in stocks:
                if not isinstance(s, str):
                    raise AttributeError(
                        "Stock must be string type", name="stocks")
            if aggregation_timeframe is None:
                aggregation_timeframe = step_timeframe
            self.data.append(MarketConfig([StockConfig(
                s, aggregation_timeframe) for s in stocks], step_timeframe, from_dt, untill_dt))
            return self

        def add_stock(self, stock: str, step_timeframe: TimeFrame, from_dt: date, untill_dt: date, aggregation_timeframe: TimeFrame = None) -> MarketConfigSet.Builder:
            return self.add_stocks([stock], step_timeframe, from_dt, untill_dt, aggregation_timeframe)

        def add_stocks_set(self, stocks_set: List[List[str]], step_timeframe: TimeFrame, from_dt: date, untill_dt: date, aggregation_timeframe: TimeFrame = None) -> MarketConfigSet.Builder:
            for stocks in stocks_set:
                if isinstance(stocks, str):
                    raise AttributeError("Stocks set must contain list of stocks set.",name="stocks_set")
                self.add_stocks(stocks, step_timeframe, from_dt,
                                untill_dt, aggregation_timeframe)
            return self

        def build(self) -> MarketConfigSet:
            return MarketConfigSet(self.data)

    def __init__(self, data: List[MarketConfig] = []):
        if len(data) == 0:
            raise AttributeError("Cann't set no market configs")
        self.__data: Tuple = tuple(data)

    def as_records(self) -> List[MarketConfig]:
        return [rec for rec in self.__data]
