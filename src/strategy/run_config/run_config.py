from __future__ import annotations
from typing import Dict
from .market_config import MarketConfig
from .strategy_config import StrategyConfig
from .strategy_id import StrategyId


class RunConfig:
    """configuration of single strategy run
    """
    MARKET_CFG_F = "market_cfg"
    STRATEGY_CFG_F = "strategy_cfg"

    def __init__(self, market_config: MarketConfig, strategy_cfg: StrategyConfig = StrategyConfig()):
        # Convert to a tuple to make it immutable
        self._market_cfg = market_config
        self._strategy_cfg = strategy_cfg

    @property
    def market_cfg(self) -> MarketConfig:
        """Configuration of market data
        """
        return self._market_cfg

    @property
    def strategy_cfg(self) -> StrategyConfig:
        """Strategy configuration parameter
        """
        return self._strategy_cfg

    def to_dict(self) -> Dict:
        return {
            RunConfig.MARKET_CFG_F: self.market_cfg.to_dict(),
            RunConfig.STRATEGY_CFG_F: dict(self.strategy_cfg),
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((self.market_cfg, self.strategy_cfg))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RunConfig):
            return False
        return self.to_dict() == other.to_dict()
