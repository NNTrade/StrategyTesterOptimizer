from abc import ABC, abstractmethod
from typing import List
from .optimization_market_config_tuple import OptimizationMarketConfigTuple
from ...strategy.run_config import MarketConfig
from datetime import timedelta

class absMarketConfigSplitter(ABC):
  MIN_RELATION = 1/8
  MAX_RELATION = 1/4
  def __init__(self, optimization_td:timedelta, forward_td:timedelta, forced_split:bool = False):
    self.optimization_td = optimization_td
    self.forward_td = forward_td
    self.forced_split = forced_split
    if not self.forced_split:
      interval_rel = self.forward_td / self.optimization_td
      if interval_rel < absMarketConfigSplitter.MIN_RELATION or interval_rel > absMarketConfigSplitter.MAX_RELATION:
          raise AttributeError(f"Wrong relation between optimization interval and forward interval ({interval_rel}). It must be between {absMarketConfigSplitter.MIN_RELATION}-{absMarketConfigSplitter.MAX_RELATION}")        
    
  @abstractmethod
  def split(self, market_config:MarketConfig)->List[OptimizationMarketConfigTuple]:
    ...

