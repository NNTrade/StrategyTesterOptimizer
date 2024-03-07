from ..report_comparer.realization.by_yield_per_year import ByYieldPerYear
from ..config import StrategyConfigSet
from ..strategy.abs_strategy import absStrategy,absReportComparer
from abc import ABC, abstractmethod

class absStrategyFactory(ABC):
   def __init__(self, run_report_comparer:absReportComparer|None = None) -> None:
     self._run_report_comparer = run_report_comparer if run_report_comparer is not None else ByYieldPerYear()
     super().__init__()

   @abstractmethod
   def build(self,strategy_config_set:StrategyConfigSet)->absStrategy:
     ...