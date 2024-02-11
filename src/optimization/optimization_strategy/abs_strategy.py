from __future__ import annotations
from abc import ABC, abstractmethod

from ...simulation.models.simulation_report import SimulationReport
from .comparers import by_strategy_yield_per_year_comparer
from ..config import StrategyConfigSet, StrategyConfig
from typing import Union, Callable

"""Parameter optimization strategy. Realization of this class realize strategy of parameter optimization

Returns:
    _type_: _description_
"""
class absStrategy(ABC):
  def __init__(self,strategy_config_set:StrategyConfigSet, run_report_comparer:Callable[[SimulationReport,SimulationReport],int] = by_strategy_yield_per_year_comparer) -> None:
    self._strategy_config_set = strategy_config_set
    self._run_report_comparer = run_report_comparer
    self.__best_rr = None
    super().__init__()
  
  @abstractmethod
  def first(self)->StrategyConfig:
    ...
  
  def next(self,last_simulation_report:SimulationReport)->Union[StrategyConfig, None]:
    self._update_best_run_report(last_simulation_report)

    return self._get_next(last_simulation_report)
  
  def _update_best_run_report(self,prev_run_report:SimulationReport):
    if self.__best_rr is None:
      self.__best_rr = prev_run_report
    else:
      if self._run_report_comparer(self.__best_rr, prev_run_report) > 0:
        self.__best_rr = prev_run_report

  @abstractmethod
  def _get_next(self,prev_run_report:SimulationReport)->Union[StrategyConfig, None]:
    ...

  def best(self)->Union[SimulationReport, None]:
    return self.__best_rr
  
