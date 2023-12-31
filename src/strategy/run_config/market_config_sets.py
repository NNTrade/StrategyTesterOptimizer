from __future__ import annotations
from typing import Tuple, List, Callable
from datetime import date

from .is_valid_checker import IsValidChecker
from .market_config import MarketConfig
from NNTrade.common import TimeFrame
from .stock_config import StockConfig
from .abs_base_config import absBaseConfigSet, absBaseBuilder


class MarketConfigSet(absBaseConfigSet[MarketConfig]):
    """Set of market configuration data
    """
    class Builder(absBaseBuilder["MarketConfigSet.Builder", MarketConfig]):
        def __init__(self) -> None:
            self.data: List[MarketConfig] = []
            super().__init__()

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
                    raise AttributeError(
                        "Stocks set must contain list of stocks set.", name="stocks_set")
                self.add_stocks(stocks, step_timeframe, from_dt,
                                untill_dt, aggregation_timeframe)
            return self

        def build(self) -> MarketConfigSet:
            return MarketConfigSet(self.data, self.is_valid_checker)

    def __init__(self, data: List[MarketConfig] = [], is_valid_checker: IsValidChecker[MarketConfig] = None) -> None:
        super().__init__(is_valid_checker)
        if len(data) == 0:
            raise AttributeError("Cann't set no market configs")
        self.__data: Tuple[MarketConfig] = tuple(data)

    def split(self, chunks_count: int) -> MarketConfigSet:
        ret_cfg = []
        for mc in self.__data:
            ret_cfg.extend(mc.split(chunks_count))
        return MarketConfigSet(ret_cfg, self.is_valid_checker)

    def _build_records(self) -> List[MarketConfig]:
        return list(self.__data)
