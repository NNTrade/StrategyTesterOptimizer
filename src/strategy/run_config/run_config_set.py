from __future__ import annotations
from typing import Callable, List
from .strategy_config_sets import StrategyConfigSet
from .market_config_sets import MarketConfigSet
from .run_config import RunConfig, StrategyId
from .abs_base_config import absBaseConfigSet


class RunConfigSet(absBaseConfigSet[RunConfig]):
    """Run configuration set
    """

    def __init__(self, strategy_id: StrategyId, market_cfg_set: MarketConfigSet, strategy_cfg_set: StrategyConfigSet = StrategyConfigSet(), is_valid_func: Callable[[RunConfig], bool] = None) -> None:
        self.__market_cfg_set = market_cfg_set
        self.__strategy_cfg_set = strategy_cfg_set
        self.__strategy_id = strategy_id
        super().__init__(is_valid_func)
        pass

    @property
    def strategy_id(self) -> StrategyId:
        """Strategy id
        """
        return self.__strategy_id

    @property
    def market_cfg_set(self) -> MarketConfigSet:
        """Set of market data configurations
        """
        return self.__market_cfg_set

    @property
    def strategy_cfg_set(self) -> StrategyConfigSet:
        """Set of strategy configurations
        """
        return self.__strategy_cfg_set

    def _build_records(self) -> List[RunConfig]:
        _ret = []
        for m_rec in self.__market_cfg_set.as_records():
            for s_rec in self.__strategy_cfg_set.as_records():
                _ret.append(RunConfig(self.__strategy_id, m_rec, s_rec))
        return _ret
