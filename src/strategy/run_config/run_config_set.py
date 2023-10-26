from __future__ import annotations
from datetime import date
from itertools import product
from typing import Callable, Dict, Iterable, List, Tuple
from .strategy_config_sets import StrategyConfigSets

# TODO [FI-88]: Переделать RunConfigSet


class RunConfigSet:
    """Container of testing or optimization running config

    """
    @staticmethod
    def buildSameTradeInterval(stock_list: List[str], from_date: date, untill_date: date, strategy_parameters: StrategyConfigSets = StrategyConfigSets()) -> RunConfigSet:
        stocks_dic = {s: (from_date, untill_date) for s in stock_list}
        return RunConfigSet(stocks_dic, strategy_parameters)

    def __init__(self, stocks: Dict[str, Tuple[date, date]], strategy_parameters: StrategyConfigSets = StrategyConfigSets()) -> None:
        for from_date, untill_date in stocks.values():
            if from_date >= untill_date:
                raise AttributeError("From date must be less then untill date")

        self.__stocks = stocks
        self.__parameters = strategy_parameters
        pass

    @property
    def stocks(self) -> Dict[str, Tuple[date, date]]:
        return self.__stocks.copy()

    @property
    def strategy_parameters(self) -> StrategyConfigSets:
        return self.__parameters
