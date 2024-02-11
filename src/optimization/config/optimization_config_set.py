from typing import Generic, List

from src.simulation.config.strategy_config import StrategyConfig
from .strategy_config_sets import T, StrategyConfigSet
from ...simulation.config import SimulationConfig, MarketConfig

class OptimizationConfigSet(Generic[T]):
    """Run configuration set
    """

    def __init__(self, market_cfg: MarketConfig, strategy_cfg_set: StrategyConfigSet[T]) -> None:
        self.__market_cfg = market_cfg
        self.__strategy_cfg_set = strategy_cfg_set
        super().__init__()
        pass

    @property
    def market_cfg(self) -> MarketConfig:
        """Set of market data configurations
        """
        return self.__market_cfg

    @property
    def strategy_cfg_set(self) -> StrategyConfigSet:
        """Set of strategy configurations
        """
        return self.__strategy_cfg_set

    def as_records(self) -> List[SimulationConfig]:
        _ret = []
        for s_rec in self.__strategy_cfg_set.as_records():
            _ret.append(SimulationConfig(self.__market_cfg, s_rec))
        return _ret
    
