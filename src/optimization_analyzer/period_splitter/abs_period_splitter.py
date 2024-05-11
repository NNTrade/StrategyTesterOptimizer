from abc import ABC, abstractmethod
from typing import List
from ..config import AnalyzationPeriod
from ...common import DatePeriod
from datetime import timedelta

class absPeriodSplitter(ABC):
  MIN_RELATION = 1/8
  MAX_RELATION = 1/4
  def __init__(self, optimization_td:timedelta, forward_td:timedelta, forced_split:bool = False):
    self._optimization_td = optimization_td
    self._forward_td = forward_td
    self.forced_split = forced_split
    if not self.forced_split:
      interval_rel = self._forward_td / self._optimization_td
      if interval_rel < absPeriodSplitter.MIN_RELATION or interval_rel > absPeriodSplitter.MAX_RELATION:
          raise AttributeError(f"Wrong relation between optimization interval and forward interval ({interval_rel}). It must be between {absPeriodSplitter.MIN_RELATION}-{absPeriodSplitter.MAX_RELATION}")        
    
  @abstractmethod
  def split(self, date_period:DatePeriod)->List[AnalyzationPeriod]:
    ...