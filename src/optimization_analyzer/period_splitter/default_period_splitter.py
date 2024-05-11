from __future__ import annotations
import logging
from .abs_period_splitter import absPeriodSplitter, DatePeriod, AnalyzationPeriod
from datetime import timedelta
from typing import List
from ...splitter import DatePeriodSplitter

class DefaultPeriodSplitter(absPeriodSplitter):
  @staticmethod
  def from_days(optimization_days:int, forward_days:int, forced_split:bool = False, cut_tail:bool = True)->DefaultPeriodSplitter:
    return DefaultPeriodSplitter(timedelta(optimization_days), timedelta(forward_days),forced_split,cut_tail)
  
  @staticmethod
  def default_tf_d()->DefaultPeriodSplitter:
     return DefaultPeriodSplitter.from_days(360, 60)

  def __init__(self, optimization_td:timedelta, forward_td:timedelta, forced_split:bool = False, cut_tail:bool = True):
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
    self.__logger = logging.getLogger(f"DefaultPeriodSplitter")
    self.__splitter = DatePeriodSplitter([optimization_td,forward_td], shift=forward_td,cut_tail=cut_tail)
    super().__init__(optimization_td,forward_td,forced_split)
    

  def split(self, date_period:DatePeriod)->List[AnalyzationPeriod]:
    """splitt date period to list of optimization and forward analization periods
    """
    self.__logger.info(f"Splitting {date_period} on optmization ({self._optimization_td}) and forward  ({self._forward_td}) intervals")
    splitted_arr = self.__splitter.split(date_period)

    _return = [AnalyzationPeriod(
              sub_interval[0],
              sub_interval[1]) 
            for sub_interval in splitted_arr]
    pretty_dicts = '\n'.join(f"{d}" for d in _return)
    self.__logger.debug(f"Splitted on:\n{pretty_dicts}")

    return _return
      