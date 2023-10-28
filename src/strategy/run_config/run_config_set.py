from __future__ import annotations
from datetime import date
from itertools import product
from typing import Callable, Dict, Iterable, List, Tuple
from .strategy_config_sets import StrategyConfigSet
from .market_config_sets import MarketConfigSet
from .run_config import RunConfig, StrategyId

class RunConfigSet:
    def __init__(self, strategy_id: StrategyId, market_cfg_set: MarketConfigSet, strategy_cfg_set: StrategyConfigSet = StrategyConfigSet()) -> None:
        self.__market_cfg_set = market_cfg_set
        self.__strategy_cfg_set = strategy_cfg_set
        self.__strategy_id = strategy_id
        pass

    @property
    def strategy_id(self) -> StrategyId:
        return self.__strategy_id

    @property
    def market_cfg_set(self) -> MarketConfigSet:
        return self.__market_cfg_set

    @property
    def strategy_cfg_set(self) -> StrategyConfigSet:
        return self.__strategy_cfg_set

    def as_records(self) -> List[RunConfig]:
        _ret = []
        for m_rec in self.__market_cfg_set.as_records():
            for s_rec in self.__strategy_cfg_set.as_records():
                _ret.append(RunConfig(self.__strategy_id, m_rec, s_rec))
        return _ret
