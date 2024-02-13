import logging
from typing import Tuple

from .config import OptimizationConfig
from .strategy import absStrategyFactory

from ..simulation.config import SimulationConfig
from ..simulation.report import SimulationReport
from ..simulation.abs_trading_simulatior import absTradingSimulatior

class Optimizer:
    def __init__(self, trading_simulator: absTradingSimulatior, optimization_strategy_factory: absStrategyFactory) -> None:
      self.__trading_simulator = trading_simulator
      self.__parametar_optimizator_factory = optimization_strategy_factory
      self.__logger = logging.getLogger("OptimizationReport")
      self.workerCount = None
      pass

    @property
    def trading_simulator(self)->absTradingSimulatior:
       return self.__trading_simulator
    
    def optimize(self, optimization_config_set: OptimizationConfig)->SimulationReport:
        self.__logger.info("Start optimization")

        #Get new parameter optimizator of current optimization perido
        pof = self.__parametar_optimizator_factory.build(optimization_config_set.strategy_cfg_set)

        sc = pof.first()
        while sc is not None:
          sc = SimulationConfig(optimization_config_set.candle_ds_cfg, optimization_config_set.period, sc)
          sr = self.__trading_simulator.get_report(sc)
          sc = pof.next(sr)
          
        best_opt_sr = pof.best()

        if best_opt_sr is None:
           raise Exception("No simulation report has been found")
        
        return best_opt_sr