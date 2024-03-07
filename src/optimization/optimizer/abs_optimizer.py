from abc import ABC, abstractmethod
from ...simulation import absTradingSimulatior, StrategyId, SimulationReport
from ..config import OptimizationConfig,SimulationConfig
from ..strategy import absStrategyFactory
from ..strategy.realization import GridStrategyFactory
from typing import List,Tuple
import logging


class AbsOptimizer(ABC):
    def __init__(self, realization: str|type, trading_simulator: absTradingSimulatior, optimization_strategy_factory: absStrategyFactory | None = None) -> None:
        self.__trading_simulator = trading_simulator
        self._parametar_optimizator_factory = optimization_strategy_factory if optimization_strategy_factory is not None else GridStrategyFactory()
        self.__logger = logging.getLogger("AbsOptimizer")

        if isinstance(realization, str):
            realization_name = realization
        elif isinstance(realization, type):
            realization_name = realization.__name__
        else:
            raise AttributeError("Wrong type of realization parameter", "realization", realization)

        self._logger = self.__logger.getChild(realization_name)
        pass

    @property
    def trading_simulator(self) -> absTradingSimulatior:
        return self.__trading_simulator
    
    @abstractmethod
    def optimize(self, strategy_id: StrategyId, optimization_config_set: OptimizationConfig) -> Tuple[SimulationConfig,List[SimulationReport]]:
        ...