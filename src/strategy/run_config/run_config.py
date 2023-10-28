from __future__ import annotations
from typing import Dict
from .market_config import MarketConfig
from .strategy_config import StrategyConfig
from .strategy_id import StrategyId


class RunConfig:
    STRATEGY_ID_F = "strategy_id"
    MARKET_CFG_F = "market_cfg"
    STRATEGY_CFG_F = "strategy_cfg"
    """configuration of single strategy run
    """

    def __init__(self, strategy_id: StrategyId, market_config: MarketConfig, strategy_cfg: StrategyConfig = StrategyConfig()):
        # Convert to a tuple to make it immutable
        self._strategy_id = strategy_id
        self._market_cfg = market_config
        self._strategy_cfg = strategy_cfg

    @property
    def strategy_id(self) -> StrategyId:
        return self._strategy_id

    @property
    def market_cfg(self) -> MarketConfig:
        return self._market_cfg

    @property
    def strategy_cfg(self) -> StrategyConfig:
        return self._strategy_cfg

    def to_dict(self) -> Dict:
        return {
            RunConfig.STRATEGY_ID_F: self.strategy_id.to_dict(),
            RunConfig.MARKET_CFG_F: self.market_cfg.to_dict(),
            RunConfig.STRATEGY_CFG_F: dict(self.strategy_cfg),
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((self.strategy_id, self.market_cfg, self.strategy_cfg))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RunConfig):
            return False
        return self.to_dict() == other.to_dict()
