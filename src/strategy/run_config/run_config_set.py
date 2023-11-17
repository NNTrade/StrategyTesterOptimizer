from __future__ import annotations
from typing import Callable, List,Union
from .strategy_config_sets import StrategyConfigSet
from .market_config_sets import MarketConfigSet
from .run_config import RunConfig, StrategyId
from .abs_base_config import absBaseConfigSet,IsValidChecker


class RunConfigSet(absBaseConfigSet[RunConfig]):
    """Run configuration set
    """

    def __init__(self, market_cfg_set: MarketConfigSet, strategy_cfg_set: StrategyConfigSet = StrategyConfigSet(), is_valid_func: Union[IsValidChecker[RunConfig],None] = None) -> None:
        self.__market_cfg_set = market_cfg_set
        self.__strategy_cfg_set = strategy_cfg_set
        super().__init__(is_valid_func)
        pass

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
                _ret.append(RunConfig(m_rec, s_rec))
        return _ret
