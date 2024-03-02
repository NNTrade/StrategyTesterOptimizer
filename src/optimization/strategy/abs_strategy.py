from __future__ import annotations
from abc import ABC, abstractmethod
import logging

from ..report_comparer.abs_report_comparer import absReportComparer
from ..report_comparer.realization import ByYieldPerYear

from ...simulation.report.simulation_report import SimulationReport
from ..config import StrategyConfigSet, StrategyConfig
from typing import Union, Callable

"""Parameter optimization strategy. Realization of this class realize strategy of parameter optimization

Returns:
    _type_: _description_
"""
class absStrategy(ABC):
  def __init__(self,strategy_config_set:StrategyConfigSet, run_report_comparer:Union[absReportComparer,None] = None, comparer_name:Union[str,None]=None) -> None:
    self._strategy_config_set = strategy_config_set
    self._run_report_comparer = run_report_comparer if run_report_comparer is not None else ByYieldPerYear()
    self.__best_rr = None
    self.__logger = logging.getLogger("absStrategy")
    self._logger = self.__logger if comparer_name is None else self.__logger.getChild(comparer_name)
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
      if self._run_report_comparer.comparer(self.__best_rr, prev_run_report) > 0:
        self.__logger.info(f"report on {self.__best_rr.simulation_config.strategy_cfg} is worst than last {prev_run_report.simulation_config.strategy_cfg}")
        self.__best_rr = prev_run_report

  @abstractmethod
  def _get_next(self,prev_run_report:SimulationReport)->Union[StrategyConfig, None]:
    ...

  def best(self)->Union[SimulationReport, None]:
    return self.__best_rr
  
