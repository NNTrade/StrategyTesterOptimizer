from .abs_parameter_optimizator import absParameterOptimizator, Callable,RunReport
from ..strategy.run_config import StrategyConfigSet
from abc import ABC, abstractmethod
from .comparer import by_strategy_yield_per_year_comparer

class absParameterOptimizatorFactory(ABC):
  def __init__(self, run_report_comparer:Callable[[RunReport,RunReport],int] = by_strategy_yield_per_year_comparer) -> None:
    self._run_report_comparer = run_report_comparer
    super().__init__()
    
  @abstractmethod
  def build(self,strategy_config_set:StrategyConfigSet)->absParameterOptimizator:
    ...