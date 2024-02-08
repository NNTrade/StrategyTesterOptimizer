import logging
from typing import Tuple

from ..simulation.config import SimulationConfig
from ..simulation.models import SimulationReport
from ..simulation.abs_trading_simulation_factory import absTradingSimulationFactory

from .market_config_splitter.optimization_market_config_tuple import OptimizationMarketConfigTuple
from .config.simulation_config_set import SimulationConfigSet
from .parameter_optimizator.abs_parameter_optimizator_factory import absParameterOptimizatorFactory


class Worker:
      def __init__(self,run_report_factory: absTradingSimulationFactory,
                        parametar_optimizator_factory: absParameterOptimizatorFactory,
                        simulation_config_set: SimulationConfigSet, 
                        mc_chunks_arr_total:int, 
                        logger: logging.Logger, 
                        ) -> None:
        self.__run_config_set= simulation_config_set
        self.__total = mc_chunks_arr_total
        self.__logger = logger
        self.__run_report_factory = run_report_factory
        self.__parametar_optimizator_factory = parametar_optimizator_factory
        pass

      def do_args(self, args)->Tuple[SimulationReport,SimulationReport]:
        idx = args[0]
        mc_set = args[1]
        return self.do(idx,mc_set)
      
      def do(self,idx, mc_set:OptimizationMarketConfigTuple)->Tuple[SimulationReport,SimulationReport]:
        self.__logger.info("Start optimization tuple %i/%i",idx+1,self.__total)

          #Get new parameter optimizator of current optimization perido
        pof = self.__parametar_optimizator_factory.build(self.__run_config_set.strategy_cfg_set)

        best_opt_rr = None

        #While parameter optimizator doesn't return best RunConfig continue checking
        while best_opt_rr is None:
          sc = pof.first()
          while sc is not None:
            opt_rc = SimulationConfig(mc_set.optimization_config, sc)
            opt_rr = self.__run_report_factory.get(opt_rc)
            sc = pof.next(opt_rr)
          
          best_opt_rr = pof.best()

        fwd_rc = SimulationConfig(mc_set.forward_config, best_opt_rr.simulation_config.strategy_cfg)
        fwd_rr = self.__run_report_factory.get(fwd_rc)
        return (best_opt_rr,fwd_rr)