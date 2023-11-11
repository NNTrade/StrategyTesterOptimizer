from __future__ import annotations
from .strategy.run_report import RunReportFactory,RunReport
from .strategy.run_config import RunConfigSet,RunConfig
from .optimization.config import OptimizatianConfig
from datetime import timedelta
from typing import List,Tuple
from .optimization.abs_parameter_optimizator_factory import absParameterOptimizatorFactory
from .optimization.market_config_splitter import absMarketConfigSplitter,DefaultMarketConfigSplitter


class OptimizationReport:
  class Factory:
    def __init__(self, runReportFactory: RunReportFactory, parametar_optimizator_factory: absParameterOptimizatorFactory, market_config_splitter: absMarketConfigSplitter = None) -> None:
      self.__run_report_factory = runReportFactory
      self.__parametar_optimizator_factory = parametar_optimizator_factory
      self.__market_config_splitter = DefaultMarketConfigSplitter.default_tf_d() if market_config_splitter is None else market_config_splitter
      pass

    def get(self, run_config_set: RunConfigSet)->OptimizationReport:
      rr_list = []
      #Loop all avaliable market configs
      for mc in run_config_set.market_cfg_set.as_records():
        
        #Split all market config on optimization and forward chunks
        mc_set_arr = self.__market_config_splitter.split(mc)

        for mc_set in mc_set_arr:
          
          #Get new parameter optimizator of current optimization perido
          pof = self.__parametar_optimizator_factory.build(run_config_set.strategy_cfg_set)

          best_opt_rr = None

          #While parameter optimizator doesn't return best RunConfig continue checking
          while best_opt_rr is None:

            sc = pof.first()
            while sc is not None:
              opt_rc = RunConfig(run_config_set.strategy_id, mc_set.optimization_config, sc)
              opt_rr = self.__run_report_factory.get(opt_rc)
              sc = pof.next(opt_rr)
          
            best_opt_rr = pof.best()

          fwd_rc = RunConfig(run_config_set.strategy_id, mc_set.forward_config, best_opt_rr.run_config.strategy_cfg)
          fwd_rr = self.__run_report_factory.get(fwd_rc)
          rr_list.append((best_opt_rr,fwd_rr))
      return OptimizationReport(rr_list)
          

  def __init__(self,run_report_list: List[Tuple[RunReport,RunReport]]) -> None:
    pass