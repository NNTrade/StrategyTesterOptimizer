import logging
from ..abs_strategy_factory import absStrategyFactory

from ..abs_strategy import absStrategy,StrategyConfigSet, StrategyConfig,SimulationReport, Union,Callable,absReportComparer


"""Factory for creating grid search strategy for parameter optimization
"""
class GridStrategyFactory(absStrategyFactory):
  def __init__(self, run_report_comparer:Union[absReportComparer,None] = None) -> None:
    super().__init__(run_report_comparer)

  def build(self,strategy_config_set:StrategyConfigSet)->absStrategy:
    return GridStrategy(strategy_config_set, self._run_report_comparer)
    
"""Grid search strategy for parameter optimization

Returns:
    _type_: _description_
"""
class GridStrategy(absStrategy):    
  def __init__(self,strategy_config_set:StrategyConfigSet, run_report_comparer:Union[absReportComparer,None] = None) -> None:
    super().__init__(strategy_config_set, run_report_comparer,"GridStrategy")
    self.__avaliable_str_cfg = self._strategy_config_set.as_records()
  
  def first(self)->StrategyConfig:
    first_cfg = self.__avaliable_str_cfg.pop()
    self._logger.info(f"Get first strategy config:\n{first_cfg}")
    return first_cfg
  
  def _get_next(self,prev_run_report:SimulationReport)->Union[StrategyConfig, None]:
    try:
      next_cfg = self.__avaliable_str_cfg.pop()
      self._logger.info(f"Get next strategy config:\n{next_cfg}")
      return next_cfg
    except IndexError:
      return None
  