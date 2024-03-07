from __future__ import annotations
import pprint
from typing import Dict, MutableMapping, Union
import json

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
    
    def to_dict(self) -> Dict:
        return self.__data

    def __str__(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.__str__()
    
    def to_json(self):
        return json.dumps(self.__data)

    @classmethod
    def from_json(cls, json_str):
        return cls(json.loads(json_str))
