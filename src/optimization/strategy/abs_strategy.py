from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from ..report_comparer.abs_report_comparer import absReportComparer
from ..report_comparer.realization import ByYieldPerYear
from ...simulation.report.simulation_report import SimulationReport,SimulationConfig
from ..config import StrategyConfigSet, StrategyConfig
from typing import List,Tuple

"""Parameter optimization strategy. Realization of this class realize strategy of parameter optimization

Returns:
    _type_: _description_
"""
class absStrategy(ABC):
  def __init__(self,comparer:str|type, strategy_config_set:StrategyConfigSet, run_report_comparer:absReportComparer) -> None:
    if isinstance(comparer, str):
        comparer_name = comparer
    elif isinstance(comparer, type):
        comparer_name = comparer.__name__
    else:
        raise AttributeError("Wrong type of comparer parameter", "comparer", comparer)
    self._strategy_config_set = strategy_config_set
    self._run_report_comparer = run_report_comparer
    self.__best_rr:Tuple[StrategyConfig,List[SimulationReport]]|None = None
    self.__logger = logging.getLogger("absStrategy")
    self._logger = self.__logger if comparer_name is None else self.__logger.getChild(comparer_name)
    super().__init__()
  
  @abstractmethod
  def first(self)->StrategyConfig:
    ...
  
  def __are_all_values_equal(self,arr):
    # Check if the array is empty
    if not arr:
        return True  # If array is empty, all values are considered equal (trivially true)

    # Compare each value to the first value in the array
    first_value = arr[0]
    for value in arr[1:]:
        if value != first_value:
            return False  # If any value is not equal to the first value, return False
    
    return True  # If all values are equal, return True
  
  def next(self,last_simulation_reports:List[SimulationReport])->StrategyConfig|None:
    self._update_best_run_report(last_simulation_reports)

    return self._get_next(last_simulation_reports)
  
  def _update_best_run_report(self,prev_run_reports:List[SimulationReport]):
    assert len(prev_run_reports) > 0, "Receive no reports"
    assert self.__are_all_values_equal([sr.simulation_config.strategy_cfg for sr in prev_run_reports]), "Not all reports based on same StrategyConfig"
    
    if self.__best_rr is None:
      self.__best_rr = prev_run_reports[0].simulation_config.strategy_cfg,prev_run_reports
    else:
      if self._run_report_comparer.comparer(self.__best_rr[1], prev_run_reports) > 0:
        self.__logger.debug(f"report on {[rr.simulation_config.strategy_cfg for rr in self.__best_rr[1]]} is worst than last {[rr.simulation_config.strategy_cfg for rr in prev_run_reports]}")
        self.__best_rr = prev_run_reports[0].simulation_config.strategy_cfg,prev_run_reports

  @abstractmethod
  def _get_next(self,prev_run_report:List[SimulationReport])->StrategyConfig| None:
    ...

  def best(self)->Tuple[StrategyConfig,List[SimulationReport]]|None:
    return self.__best_rr
  
