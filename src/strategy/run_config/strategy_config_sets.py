from __future__ import annotations
from itertools import product
from typing import Callable, Dict, List, MutableMapping
from .strategy_config import StrategyConfig


class StrategyConfigSet(MutableMapping):
    """Strategy parameters set
    """
    class Builder:
        def __init__(self) -> None:
            self.data = {}
            self.validation_func: Callable[[Dict], bool] = lambda config: True
            pass

        def add_set(self, parameterName, parameterSet: List) -> StrategyConfigSet.Builder:
            self.data[parameterName] = parameterSet
            return self

        def add_validation_func(self, validation_func: Callable[[Dict], bool]) -> StrategyConfigSet.Builder:
            self.validation_func = validation_func
            return self

        def build(self) -> StrategyConfigSet:
            return StrategyConfigSet(self.data, self.validation_func)

    def __init__(self, data={}, validation_func: Callable[[Dict], bool] = lambda config: True):
        self.__data = data
        self.__is_valid_func = validation_func

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        raise Exception("Set value is not avaliable")

    def __delitem__(self, key):
        raise Exception("Delete is not avaliable")

    def __iter__(self):
        return iter(self.__data)

    def __len__(self):
        return len(self.__data)

    def as_records(self) -> List[StrategyConfig]:
        if len(self.__data) == 0:
            return []
        ret_list = [dict(zip(self.__data.keys(), combo))
                    for combo in product(*self.__data.values())]
        return [StrategyConfig(r) for r in ret_list if self.__is_valid_func(r)]

    @property
    def is_valid_func(self) -> Callable[[Dict], bool]:
        return self.__is_valid_func
