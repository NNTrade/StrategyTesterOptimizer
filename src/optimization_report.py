from __future__ import annotations
from .strategy.run_report import RunReportFactory,RunReport
from .strategy.run_config import RunConfigSet,RunConfig
from typing import List,Tuple
from .optimization.parameter_optimizator import absParameterOptimizatorFactory
from .optimization.market_config_splitter import absMarketConfigSplitter,DefaultMarketConfigSplitter
import logging
import concurrent.futures
import multiprocessing

class OptimizationReport:
  class Factory:
    def __init__(self, runReportFactory: RunReportFactory, parametar_optimizator_factory: absParameterOptimizatorFactory, market_config_splitter: absMarketConfigSplitter = None) -> None:
      self.__run_report_factory = runReportFactory
      self.__parametar_optimizator_factory = parametar_optimizator_factory
      self.__market_config_splitter = DefaultMarketConfigSplitter.default_tf_d() if market_config_splitter is None else market_config_splitter
      self.__logger = logging.getLogger("OptimizationReport")
      self.workerCount = None
      pass

    def get(self, run_config_set: RunConfigSet)->OptimizationReport:
      if self.workerCount is None:
        self.workerCount = multiprocessing.cpu_count()
      assert self.workerCount > 0, "No workers"

      rr_list = []
      #Loop all avaliable market configs
      mcs_recs = run_config_set.market_cfg_set.as_records()
      mcs_recs_total = len(mcs_recs)
      for idx, mc in enumerate(mcs_recs):
        self.__logger.info("Start %i/%i",idx+1,mcs_recs_total)
        mc_logger = self.__logger.getChild(f"{idx+1}/{mcs_recs_total}")

        #Split all market config on optimization and forward chunks
        mc_set_arr = self.__market_config_splitter.split(mc)
        mc_set_arr_total = len(mc_set_arr)

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.workerCount) as executor:
          # Map the do function to the list of tasks
          run_tpl = [(run_config_set, rr_list, idx, mc_logger, mc_set_arr_total, mc_set) for idx,mc_set in enumerate(mc_set_arr)]
          executor.map(self.optimization_on_market_config_sets, run_tpl)
          #for idx,mc_set in enumerate(mc_set_arr):
          #  self.optimization_on_market_config_sets(run_config_set, rr_list, idx, mc_logger, mc_set_arr_total, mc_set)
      return OptimizationReport(rr_list)

    def optimization_on_market_config_sets(self, run_config_set, rr_list, idx, mc_logger, mc_set_arr_total, mc_set):
        mc_logger.info("Start optimization tuple %i/%i",idx+1,mc_set_arr_total)

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
          

  def __init__(self,run_report_list: List[Tuple[RunReport,RunReport]]) -> None:
    self.__run_report_list = run_report_list
    pass

  @property
  def optimization_reports(self)->List[RunReport]:
    return [rt[0] for rt in self.__run_report_list]
  
  @property
  def forward_reports(self)->List[RunReport]:
    return [rt[1] for rt in self.__run_report_list]
  
  @property
  def reports_tuples(self)->List[Tuple[RunReport,RunReport]]:
    return self.__run_report_list.copy()