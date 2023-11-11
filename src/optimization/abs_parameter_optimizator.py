from __future__ import annotations
from abc import ABC, abstractmethod
from .comparer import by_strategy_yield_per_year_comparer
from ..strategy.run_config import StrategyConfigSet,StrategyConfig
from ..strategy.run_report import RunReport
from typing import Union, Callable

class absParameterOptimizator(ABC):
  def __init__(self,strategy_config_set:StrategyConfigSet, run_report_comparer:Callable[[RunReport,RunReport],int] = by_strategy_yield_per_year_comparer) -> None:
    self._strategy_config_set = strategy_config_set
    self._run_report_comparer = run_report_comparer
    super().__init__()
  
  @abstractmethod
  def first(self)->StrategyConfig:
    ...
  
  def next(self,prev_run_report:RunReport)->Union[StrategyConfig, None]:
    self._update_best_run_report(prev_run_report)

    return self._get_next(prev_run_report)
  
  def _update_best_run_report(self,prev_run_report:RunReport):
    if self.__best_rr is None:
      self.__best_rr = prev_run_report
    else:
      if self._run_report_comparer(self.__best_rr, prev_run_report) > 0:
        self.__best_rr = prev_run_report

  @abstractmethod
  def _get_next(self,prev_run_report:RunReport)->Union[StrategyConfig, None]:
    ...

  @abstractmethod
  def best(self)->Union[RunReport, None]:
    ...
  
