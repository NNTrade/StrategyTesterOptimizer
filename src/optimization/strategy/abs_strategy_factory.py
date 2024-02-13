from src.optimization.config import StrategyConfigSet
from src.optimization.strategy.abs_strategy import absStrategy
from src.optimization.strategy.comparers import by_strategy_yield_per_year_comparer
from src.simulation.report import SimulationReport


from abc import ABC, abstractmethod
from typing import Callable


class absStrategyFactory(ABC):
   def __init__(self, run_report_comparer:Callable[[SimulationReport,SimulationReport],int] = by_strategy_yield_per_year_comparer) -> None:
     self._run_report_comparer = run_report_comparer
     super().__init__()

   @abstractmethod
   def build(self,strategy_config_set:StrategyConfigSet)->absStrategy:
     ...