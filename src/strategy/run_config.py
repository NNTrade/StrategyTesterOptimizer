from __future__ import annotations
from types import MappingProxyType
from typing import List, Dict, Tuple, Iterable, Callable
from datetime import date
from itertools import product
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class RunConfig:
    # TODO: [FI-82] Описать RunConfig
    """configuration of single strategy run
    """

    def __init__(self, stock_list: List[str], from_date: date, until_date: date, parameters: Dict = {}):
        # Convert to a tuple to make it immutable
        self._stock_list = tuple(stock_list)
        self._from_date = from_date
        self._until_date = until_date
        self._parameters = MappingProxyType(parameters)

    @property
    def stock_list(self) -> List[str]:
        return self._stock_list

    @property
    def from_date(self) -> date:
        return self._from_date

    @property
    def until_date(self) -> date:
        return self._until_date

    @property
    def parameters(self) -> Dict:
        return self._parameters

class RunConfigSet:
    """Container of testing or optimization running config

    """
    @staticmethod
    def buildSameTradeInterval(stock_list: List[str], from_date: date, untill_date: date, parameters: Dict[str, Iterable] = {}, validation_func: Callable[[Dict], bool] = lambda config: True) -> RunConfigSet:
        stocks_dic = {s: (from_date, untill_date) for s in stock_list}
        return RunConfigSet(stocks_dic, parameters, validation_func)

    def __init__(self, stocks: Dict[str, Tuple[date, date]], parameters: Dict[str, Iterable] = {}, validation_func: Callable[[Dict], bool] = lambda config: True) -> None:
        for from_date, untill_date in stocks.values():
            if from_date >= untill_date:
                raise AttributeError("From date must be less then untill date")

        self.__stocks = stocks
        self.__parameters = parameters
        self.__is_valid_func = validation_func
        pass

    @property
    def stocks(self) -> Dict[str, Tuple[date, date]]:
        return self.__stocks.copy()

    @property
    def parameters(self) -> Dict[str, Iterable]:
        return {k: [v for v in arr] for k, arr in self.__parameters.items()}

    @property
    def records(self) -> List[Dict]:
        ret_list = [dict(zip(self.__parameters.keys(), combo))
                    for combo in product(*self.__parameters.values())]
        return [r for r in ret_list if self.__is_valid_func(r)]

    @property
    def is_valid_func(self) -> Callable[[Dict], bool]:
        return self.__is_valid_func
