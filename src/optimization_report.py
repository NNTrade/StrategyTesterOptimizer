from __future__ import annotations
from .optimization.market_config_splitter.optimization_market_config_tuple import OptimizationMarketConfigTuple
from .strategy.run_report import RunReportFactory,RunReport
from .strategy.run_config import RunConfigSet,RunConfig
from typing import List,Tuple
from .optimization.parameter_optimizator import absParameterOptimizatorFactory
from .optimization.market_config_splitter import absMarketConfigSplitter,DefaultMarketConfigSplitter
import logging
import concurrent.futures
import multiprocessing
import threading

class OptimizationReport:
  class Factory:
    class Worker:
      def __init__(self,run_report_factory: RunReportFactory,
                        parametar_optimizator_factory: absParameterOptimizatorFactory,
                        run_config_set: RunConfigSet, 
                        mc_chunks_arr_total:int, 
                        logger: logging.Logger, 
                        ) -> None:
        self.__run_config_set= run_config_set
        self.__total = mc_chunks_arr_total
        self.__logger = logger
        self.__run_report_factory = run_report_factory
        self.__parametar_optimizator_factory = parametar_optimizator_factory
        pass

      def do_args(self, args)->Tuple[RunReport,RunReport]:
        idx = args[0]
        mc_set = args[1]
        return self.do(idx,mc_set)
      
      def do(self,idx, mc_set:OptimizationMarketConfigTuple)->Tuple[RunReport,RunReport]:
        self.__logger.info("Start optimization tuple %i/%i",idx+1,self.__total)

          #Get new parameter optimizator of current optimization perido
        pof = self.__parametar_optimizator_factory.build(self.__run_config_set.strategy_cfg_set)

        best_opt_rr = None

        #While parameter optimizator doesn't return best RunConfig continue checking
        while best_opt_rr is None:
          sc = pof.first()
          while sc is not None:
            opt_rc = RunConfig(self.__run_config_set.strategy_id, mc_set.optimization_config, sc)
            opt_rr = self.__run_report_factory.get(opt_rc)
            sc = pof.next(opt_rr)
          
          best_opt_rr = pof.best()

        fwd_rc = RunConfig(self.__run_config_set.strategy_id, mc_set.forward_config, best_opt_rr.run_config.strategy_cfg)
        fwd_rr = self.__run_report_factory.get(fwd_rc)
        return (best_opt_rr,fwd_rr)
      
    def __init__(self, run_report_factory: RunReportFactory, parametar_optimizator_factory: absParameterOptimizatorFactory, market_config_splitter: absMarketConfigSplitter = None) -> None:
      self.__run_report_factory = run_report_factory
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
        self.__logger.info("Start market config %i/%i",idx+1,mcs_recs_total)
        mc_logger = self.__logger.getChild(f"{idx+1}/{mcs_recs_total}")

        #Split all market config on optimization and forward chunks
        mc_set_arr = self.__market_config_splitter.split(mc)
        mc_set_arr_total = len(mc_set_arr)
        
        worker = OptimizationReport.Factory.Worker(self.__run_report_factory, self.__parametar_optimizator_factory, run_config_set, mc_set_arr_total, mc_logger)
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.workerCount) as executor:
          # Map the do function to the list of tasks
          run_tpl = [(idx,mc_set) for idx,mc_set in enumerate(mc_set_arr)]
          new_rr_list = list(executor.map(worker.do_args, run_tpl))
        
        rr_list.extend(new_rr_list)
      return OptimizationReport(rr_list)

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