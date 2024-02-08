from tkinter import NO

from .comparer import by_strategy_yield_per_year_comparer
from .abs_parameter_optimizator import absParameterOptimizator,StrategyConfigSet, StrategyConfig,SimulationReport, Union,Callable
from .abs_parameter_optimizator_factory import absParameterOptimizatorFactory


"""Grid search optimization algorithm

Returns:
    _type_: _description_
"""
class GridParameterOptimizator(absParameterOptimizator):
  class Factory(absParameterOptimizatorFactory):
    def __init__(self, run_report_comparer: Callable[[SimulationReport, SimulationReport], int] = by_strategy_yield_per_year_comparer) -> None:
      super().__init__(run_report_comparer)

    def build(self,strategy_config_set:StrategyConfigSet)->absParameterOptimizator:
      return GridParameterOptimizator(strategy_config_set, self._run_report_comparer)
    
  def __init__(self,strategy_config_set:StrategyConfigSet, run_report_comparer:Callable[[SimulationReport,SimulationReport],int]) -> None:
    super().__init__(strategy_config_set, run_report_comparer)
    self.__avaliable_str_cfg = self._strategy_config_set.as_records()
  
  def first(self)->StrategyConfig:
    return self.__avaliable_str_cfg.pop()
  
  def _get_next(self,prev_run_report:SimulationReport)->Union[StrategyConfig, None]:
    try:
      return self.__avaliable_str_cfg.pop()
    except IndexError:
      return None
  