from __future__ import annotations
from typing import Dict, MutableMapping, Union


class StrategyConfig(MutableMapping):
    """Strategy parameters
    """
    def __init__(self, data: Dict[str,Union[int, float, str]] = {}):
        self.__data = data.copy()

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
    def __hash__(self):
        # Implement a hash value based on the content of your object
        return hash(frozenset(self.__data.items()))
