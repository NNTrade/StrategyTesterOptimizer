import logging
from typing import Tuple

from .config import OptimizationConfigSet
from .strategy import absFactory

from ..simulation.config import SimulationConfig
from ..simulation.report import SimulationReport
from ..simulation.abs_trading_simulatior import absTradingSimulatior

class Optimizer:
    def __init__(self, simulation_report_factory: absTradingSimulatior, optimization_strategy_factory: absFactory) -> None:
      self.__run_report_factory = simulation_report_factory
      self.__parametar_optimizator_factory = optimization_strategy_factory
      self.__logger = logging.getLogger("OptimizationReport")
      self.workerCount = None
      pass

    def optimize(self, optimization_config_set: OptimizationConfigSet)->SimulationReport:
        self.__logger.info("Start optimization")

        #Get new parameter optimizator of current optimization perido
        pof = self.__parametar_optimizator_factory.build(optimization_config_set.strategy_cfg_set)

        sc = pof.first()
        while sc is not None:
          sc = SimulationConfig(optimization_config_set.market_cfg, sc)
          sl = self.__run_report_factory.get(sc)
          sr = SimulationReport(self.__run_report_factory.strategy_id, sc, sl)
          sc = pof.next(sr)
          
        best_opt_sr = pof.best()

        if best_opt_sr is None:
           raise Exception("No simulation report has been found")
        
        return best_opt_sr