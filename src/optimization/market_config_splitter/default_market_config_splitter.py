from __future__ import annotations
from .abs_market_config_spliter import absMarketConfigSplitter
from ...strategy.run_config import MarketConfig
from datetime import timedelta
from typing import List
from .optimization_market_config_tuple import OptimizationMarketConfigTuple

class DefaultMarketConfigSplitter(absMarketConfigSplitter):

  @staticmethod
  def default_tf_d()->DefaultMarketConfigSplitter:
     return DefaultMarketConfigSplitter(timedelta(180), timedelta(30), cut_tail=True)

  def __init__(self, optimization_td:timedelta, forward_td:timedelta, forced_split:bool = False, cut_tail:bool = False):
    self.cut_tail = cut_tail
    super().__init__(optimization_td,forward_td,forced_split)
    

  def split(self, market_config:MarketConfig)->List[OptimizationMarketConfigTuple]:
    """splitt market config to list of optimization and forward market configs
    [
      (optimization MarketConfig 1, forward MarketConfig 1),
      (optimization MarketConfig 2, forward MarketConfig 2),
    ]

    Args:
        optimization_td (timedelta): size of optimization interval
        forward_td (timedelta): size of forward interval
        forced_split (bool, optional): remove check on optimization and forward interval size relation. Defaults to False.
        cut_tail (bool, optional): remove check that if current time interval doesn't cutted sharped. Defaults to False.

    Raises:
        AttributeError: Wrong relation between optimization interval (optimization_td) and forward interval (forward_td).
        AttributeError: Cannot split interval on round parts

    Returns:
        List[Tuple[MarketConfig, MarketConfig]]: List of optimization and forward market configs
            [
                (optimization MarketConfig 1, forward MarketConfig 1),
                (optimization MarketConfig 2, forward MarketConfig 2),
            ]
    """
    return_intervals = []
    cur_dt = market_config.from_date
    forward_interval = (cur_dt,cur_dt)
    while forward_interval[1] < market_config.untill_date:
        optimization_interval = (cur_dt, cur_dt + self.optimization_td)
        forward_interval = (optimization_interval[1],optimization_interval[1]+self.forward_td)
        if forward_interval[1] <= market_config.untill_date:
            return_intervals.append((optimization_interval, forward_interval))
        elif forward_interval[1] > market_config.untill_date:
            if not self.cut_tail:
                raise AttributeError("Cannot split interval on round parts")
        cur_dt = cur_dt + self.forward_td
    return [OptimizationMarketConfigTuple(
              MarketConfig(market_config.stocks, market_config.step_timeframe, opt_interval[0], opt_interval[1]),
              MarketConfig(market_config.stocks, market_config.step_timeframe, fwd_interval[0], fwd_interval[1])) 
            for opt_interval, fwd_interval in return_intervals]
      