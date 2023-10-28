from __future__ import annotations
from datetime import date
from itertools import product
from typing import Callable, Dict, Iterable, List, Tuple
from .strategy_config_sets import StrategyConfigSets
from .market_config_sets import MarketConfigSets
from .run_config import RunConfig

class RunConfigSet:
    def __init__(self, market_cfg_set: MarketConfigSets, strategy_cfg_set: StrategyConfigSets = StrategyConfigSets()) -> None:
        self.__market_cfg_set = market_cfg_set
        self.__strategy_cfg_set = strategy_cfg_set
        pass

    @property
    def market_cfg_set(self) -> MarketConfigSets:
        return self.__market_cfg_set

    @property
    def strategy_cfg_set(self) -> StrategyConfigSets:
        return self.__strategy_cfg_set

    def as_records(self) -> List[RunConfig]:
        _ret = []
        for m_rec in self.__market_cfg_set.as_records():
            for s_rec in self.__strategy_cfg_set.as_records():
                _ret.append(RunConfig(m_rec, s_rec))
        return _ret
