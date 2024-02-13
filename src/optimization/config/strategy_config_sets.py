from __future__ import annotations
from abc import ABC
from itertools import product
from typing import Callable, Dict, List, MutableMapping, Generic, Union
from ...simulation.config import StrategyConfig
from typing import Generic, TypeVar

T = TypeVar('T',bound=StrategyConfig) 

def default_build_func(dict:Dict[str,Union[int,float,str]])->Union[StrategyConfig,None]:
    return StrategyConfig(dict)

class StrategyConfigSet(MutableMapping):
    STR_CFG_F = "strategy_cfg_set"

    """Strategy parameters set
    """
    class Builder: 
        def __init__(self) -> None:
            self.data:Dict[str,List[Union[int,float,str]]] = {}
            self.build_func = default_build_func
        
        def add_set(self, parameterName:str, parameterSet: List[Union[int,float,str]]) -> StrategyConfigSet.Builder:
            self.data[parameterName] = parameterSet
            return self
        
        def set_build_func(self, build_func: Callable[[Dict[str,Union[int,float,str]]],Union[StrategyConfig,None]]) ->  StrategyConfigSet.Builder:
            self.build_func:Callable[[Dict[str,Union[int,float,str]]],Union[StrategyConfig,None]] = build_func
            return self

        def build(self) -> StrategyConfigSet:
            return StrategyConfigSet(self.data,self.build_func)

   
    def __init__(self, 
                    data:Dict[str,List[Union[int,float,str]]]={},
                    build_func: Callable[[Dict[str,Union[int,float,str]]],Union[StrategyConfig,None]] = default_build_func):
        self.__data = data
        self.__build_func = build_func

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
    
    def as_records(self) -> List[T]:
        ret_list = []
        for data_set in [dict(zip(self.__data.keys(), combo)) for combo in product(*self.__data.values())]:
            str_cfg = self.__build_func(data_set)
            if str_cfg is not None:
                ret_list.append(str_cfg)
        return ret_list
    