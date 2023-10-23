from __future__ import annotations
from typing import List, Dict, Tuple, Iterable, Callable
from datetime import date
from itertools import product


class RunConfig:
    # TODO: [FI-82] Описать RunConfig
    """configuration of single strategy run
    """

    def __init__(self) -> None:
        pass


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
