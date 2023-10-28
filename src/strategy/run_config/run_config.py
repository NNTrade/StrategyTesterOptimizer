from __future__ import annotations
from types import MappingProxyType
from typing import List, Dict
from datetime import date
from dataclasses import dataclass
from .market_config import MarketConfig
from .strategy_config import StrategyConfig
@dataclass(unsafe_hash=True)
class RunConfig:
    """configuration of single strategy run
    """

    def __init__(self, market_config: MarketConfig, strategy_cfg: StrategyConfig = StrategyConfig()):
        # Convert to a tuple to make it immutable
        self._market_cfg = market_config
        self._strategy_cfg = strategy_cfg

    @property
    def market_cfg(self) -> MarketConfig:
        return self._market_cfg

    @property
    def strategy_cfg(self) -> StrategyConfig:
        return self._strategy_cfg
