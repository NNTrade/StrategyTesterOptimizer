from __future__ import annotations
from itertools import product
from typing import Callable, Dict, List, MutableMapping

from .is_valid_checker import IsValidChecker
from ...simulation.config import StrategyConfig
from .abs_base_config import absBaseConfigSet, absBaseBuilder


class StrategyConfigSet(MutableMapping, absBaseConfigSet):
    """Strategy parameters set
    """
    class Builder(absBaseBuilder["StrategyConfigSet.Builder", StrategyConfig]):
        def __init__(self) -> None:
            self.data = {}
            super().__init__()

        def add_set(self, parameterName, parameterSet: List) -> StrategyConfigSet.Builder:
            self.data[parameterName] = parameterSet
            return self

        def build(self) -> StrategyConfigSet:
            return StrategyConfigSet(self.data, self.is_valid_checker)

    def __init__(self, data={}, is_valid_checker: IsValidChecker[StrategyConfig] = None):
        self.__data = data
        super().__init__(is_valid_checker)

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

    def _build_records(self) -> List:
        if len(self.__data) == 0:
            return []
        ret_list = [StrategyConfig(dict(zip(self.__data.keys(), combo)))
                    for combo in product(*self.__data.values())]
        return ret_list
    