from __future__ import annotations
import logging
from .abs_period_splitter import absPeriodSplitter, DatePeriod, AnalyzationPeriod
from datetime import timedelta
from typing import List
import pprint

class DefaultPeriodSplitter(absPeriodSplitter):

  @staticmethod
  def default_tf_d()->DefaultPeriodSplitter:
     return DefaultPeriodSplitter(timedelta(180), timedelta(30), cut_tail=True)

  def __init__(self, optimization_td:timedelta, forward_td:timedelta, forced_split:bool = False, cut_tail:bool = False):
    """_summary_

    Args:
    optimization_td (timedelta): size of optimization interval
    forward_td (timedelta): size of forward interval
    forced_split (bool, optional): remove check on optimization and forward interval size relation. Defaults to False.
    cut_tail (bool, optional): remove check that if current time interval doesn't cutted sharped. Defaults to False.

    Raises:
        AttributeError: Wrong relation between optimization interval (optimization_td) and forward interval (forward_td).
        AttributeError: Cannot split interval on round parts
    """
    self.cut_tail = cut_tail
    self.__logger = logging.getLogger(f"DefaultPeriodSplitter")
    super().__init__(optimization_td,forward_td,forced_split)
    

  def split(self, date_period:DatePeriod)->List[AnalyzationPeriod]:
    """splitt date period to list of optimization and forward analization periods
    """
    self.__logger.info(f"Splitting {date_period} on optmization ({self.optimization_td}) and forward  ({self.forward_td}) intervals")
    return_intervals = []
    cur_dt = date_period.from_date
    forward_interval = (cur_dt,cur_dt)
    while forward_interval[1] < date_period.untill_date:
        optimization_interval = (cur_dt, cur_dt + self.optimization_td)
        forward_interval = (optimization_interval[1],optimization_interval[1]+self.forward_td)
        if forward_interval[1] <= date_period.untill_date:
            return_intervals.append((optimization_interval, forward_interval))
        elif forward_interval[1] > date_period.untill_date:
            if not self.cut_tail:
                raise AttributeError("Cannot split interval on round parts")
        cur_dt = cur_dt + self.forward_td
    
    
    _return = [AnalyzationPeriod(
              DatePeriod(opt_interval[0], opt_interval[1]),
              DatePeriod(fwd_interval[0], fwd_interval[1])) 
            for opt_interval, fwd_interval in return_intervals]
    pretty_dicts = '\n'.join(f"{d}" for d in _return)
    self.__logger.info(f"Splitted on:\n{pretty_dicts}")

    return _return
      