from __future__ import annotations
from .optimization_intervals_config import OptimizationIntervalsConfig
from ...strategy.run_config import List, MarketConfig, StockConfig, TimeFrame, timedelta,Dict
from dataclasses import dataclass

class OptimizationMarketSetConfig:
  @dataclass(frozen=True)
  class MarketConfigSet:
    optimication_config: MarketConfig
    forward_config: MarketConfig

  STOCKS_F = MarketConfig.STOCKS_F
  STEP_TF_F = MarketConfig.STEP_TF_F
  OPT_INT_SET_F = "optimization_interval_set"
  #TODO: [FI-94] move market_config.split_on_opt_chunks into OptimizationMarketSetConfig.build_from
  @staticmethod
  def build_from(market_config: MarketConfig, optimization_td:timedelta, forward_td:timedelta, forced_split:bool = False, cut_tail:bool = False)->OptimizationMarketSetConfig:
    mc_list = market_config.split_on_opt_chunks(optimization_td, forward_td, forced_split, cut_tail)
    return OptimizationMarketSetConfig(market_config.stocks, market_config.step_timeframe, [OptimizationIntervalsConfig.extract_from(mc1,mc2) for mc1,mc2 in mc_list])

  def __init__(self, stocks: List[StockConfig], step_timeframe: TimeFrame, optimization_interval_set: List[OptimizationIntervalsConfig]) -> None:
    self.__stocks = list(sorted(stocks, reverse=True))
    self.__step_timeframe = step_timeframe
    self.__optimization_interval_set = frozenset(optimization_interval_set)


  @property
  def stocks(self)->List[StockConfig]:
    return self.__stocks
  
  @property
  def step_timeframe(self)->TimeFrame:
    return self.__step_timeframe
  
  @property
  def optimization_interval_set(self)->List[OptimizationIntervalsConfig]:
    return list(self.__optimization_interval_set)
  
  def to_dict(self) -> Dict:
      return {
          OptimizationMarketSetConfig.STOCKS_F: [s.to_dict() for s in self.stocks],
          OptimizationMarketSetConfig.STEP_TF_F: self.step_timeframe,
          OptimizationMarketSetConfig.OPT_INT_SET_F:[s.to_dict() for s in self.optimization_interval_set],
      } 

  def __str__(self):
      return f"{self.to_dict()}"

  def __repr__(self):
      return self.__str__()

  def __hash__(self):
      # Create a hash based on a tuple of hashable attributes
      return hash((tuple(self.stocks), self.step_timeframe, tuple(self.optimization_interval_set)))

  def __eq__(self, other: object) -> bool:
      if not isinstance(other, OptimizationMarketSetConfig):
          return False
      return self.to_dict() == other.to_dict()

  def __get_opt_martket(self, opt_int_set:OptimizationIntervalsConfig)->MarketConfig:
     return MarketConfig(self.stocks, self.step_timeframe, opt_int_set.optimization_interval.from_date, opt_int_set.optimization_interval.untill_date)
  
  def __get_fwd_market(self, opt_int_set:OptimizationIntervalsConfig)->MarketConfig:
     return MarketConfig(self.stocks, self.step_timeframe, opt_int_set.optimization_interval.from_date, opt_int_set.optimization_interval.untill_date)
  
  def __get_market_cfg_set(self, opt_int_set:OptimizationIntervalsConfig)->OptimizationMarketSetConfig.MarketConfigSet:
    return OptimizationMarketSetConfig.MarketConfigSet(self.__get_opt_martket(opt_int_set),self.__get_fwd_market(opt_int_set))     

  #def to_market_config_sets(self)->List[OptimizationMarketSetConfig.MarketConfigSet]:
  #  
  #  for opt_int_set in self.optimization_interval_set:
  #     mcs = self.__get_market_cfg_set(opt_int_set)