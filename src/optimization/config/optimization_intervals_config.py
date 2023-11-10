from __future__ import annotations
from .time_interval import TimeInterval
from ...strategy.run_config import MarketConfig,Dict


class OptimizationIntervalsConfig:
  OPT_INTERVAL_F = "optimization_interval"
  FWD_INTERVAL_F = "forward_interval"
  @staticmethod
  def extract_from(optimization_market_config:MarketConfig,forward_market_config:MarketConfig)->OptimizationIntervalsConfig:
    return OptimizationIntervalsConfig(TimeInterval.extract_from(optimization_market_config),TimeInterval.extract_from(forward_market_config))

  def __init__(self, optimization_interval: TimeInterval, forward_interval:TimeInterval) -> None:
    self.__opt_interval = optimization_interval
    self.__forward_interval = forward_interval
    pass

  @property
  def optimization_interval(self)->TimeInterval:
    return self.__opt_interval
  @property
  def forward_interval(self)->TimeInterval:
    return self.__forward_interval
  
  def to_dict(self) -> Dict:
      return {
          OptimizationIntervalsConfig.OPT_INTERVAL_F: self.optimization_interval.to_dict(),
          OptimizationIntervalsConfig.FWD_INTERVAL_F: self.forward_interval.to_dict()
      }

  def __str__(self):
      return f"{self.to_dict()}"

  def __repr__(self):
      return self.__str__()

  def __hash__(self):
      # Create a hash based on a tuple of hashable attributes
      return hash((self.optimization_interval, self.forward_interval))

  def __eq__(self, other: object) -> bool:
      if not isinstance(other, OptimizationIntervalsConfig):
          return False
      return self.to_dict() == other.to_dict()
