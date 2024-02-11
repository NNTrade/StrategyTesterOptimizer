import logging
from typing import Tuple

from .config import OptimizationConfigSet
from .optimization_strategy import absFactory

from ..simulation.config import SimulationConfig
from ..simulation.report import SimulationReport
from ..simulation.abs_trading_simulation_factory import absTradingSimulationFactory

class Optimizer:
    def __init__(self, simulation_report_factory: absTradingSimulationFactory, parametar_optimizator_factory: absFactory) -> None:
      self.__run_report_factory = simulation_report_factory
      self.__parametar_optimizator_factory = parametar_optimizator_factory
      self.__logger = logging.getLogger("OptimizationReport")
      self.workerCount = None
      pass

    def optimize(self, simulation_config_set: OptimizationConfigSet)->SimulationReport:
        self.__logger.info("Start optimization")

        #Get new parameter optimizator of current optimization perido
        pof = self.__parametar_optimizator_factory.build(simulation_config_set.strategy_cfg_set)

        sc = pof.first()
        while sc is not None:
          opt_rc = SimulationConfig(simulation_config_set.market_cfg, sc)
          opt_rr = self.__run_report_factory.get(opt_rc)
          sc = pof.next(opt_rr)
          
        best_opt_sr = pof.best()

        if best_opt_sr is None:
           raise Exception("No simulation report has been found")
        
        return best_opt_sr