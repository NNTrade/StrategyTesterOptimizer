from ...strategy.run_config import MarketConfig
from dataclasses import dataclass

@dataclass(frozen=True)
class OptimizationMarketConfigTuple:
  optimization_config:MarketConfig
  forward_config:MarketConfig