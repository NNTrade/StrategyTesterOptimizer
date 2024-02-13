from ..abs_strategy_factory import absStrategyFactory

from ..comparers import by_strategy_yield_per_year_comparer
from ..abs_strategy import absStrategy,StrategyConfigSet, StrategyConfig,SimulationReport, Union,Callable


"""Factory for creating grid search strategy for parameter optimization
"""
class GridStrategyFactory(absStrategyFactory):
  def __init__(self, run_report_comparer: Callable[[SimulationReport, SimulationReport], int] = by_strategy_yield_per_year_comparer) -> None:
    super().__init__(run_report_comparer)

  def build(self,strategy_config_set:StrategyConfigSet)->absStrategy:
    return GridStrategy(strategy_config_set, self._run_report_comparer)
    
"""Grid search strategy for parameter optimization

Returns:
    _type_: _description_
"""
class GridStrategy(absStrategy):
 
    
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
  