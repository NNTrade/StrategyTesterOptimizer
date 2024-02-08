from __future__ import annotations
from .optimization.market_config_splitter.optimization_market_config_tuple import OptimizationMarketConfigTuple
from .strategy.run_report import absTradingSimulationFactory,RunReport
from .strategy.run_config import RunConfigSet,RunConfig
from typing import List,Tuple
from .optimization.parameter_optimizator import absParameterOptimizatorFactory
from .optimization.market_config_splitter import absMarketConfigSplitter,DefaultMarketConfigSplitter
import logging
import concurrent.futures
import multiprocessing

class OptimizationReport:
  class Factory:
    
      
    def __init__(self, run_report_factory: absTradingSimulationFactory, parametar_optimizator_factory: absParameterOptimizatorFactory, market_config_splitter: absMarketConfigSplitter = DefaultMarketConfigSplitter.default_tf_d()) -> None:
      self.__run_report_factory = run_report_factory
      self.__parametar_optimizator_factory = parametar_optimizator_factory
      self.__market_config_splitter = market_config_splitter
      self.__logger = logging.getLogger("OptimizationReport")
      self.workerCount = None
      pass

    def get(self, run_config_set: RunConfigSet, multi_theads:bool= True)->OptimizationReport:
      if self.workerCount is None:
        self.workerCount = multiprocessing.cpu_count()
      assert self.workerCount > 0, "No workers"

      rr_list = []

      #Loop all avaliable market configs
      mcs_recs = run_config_set.market_cfg_set.as_records()
      mcs_recs_total = len(mcs_recs)

      for idx, mc in enumerate(mcs_recs):
        self.__logger.info("Start market config %i/%i: %s",idx+1,mcs_recs_total, mc.to_dict())
        mc_logger = self.__logger.getChild(f"{idx+1}/{mcs_recs_total}")

        #Split all market config on optimization and forward chunks
        mc_set_arr = self.__market_config_splitter.split(mc)
        mc_set_arr_total = len(mc_set_arr)
        
        worker = OptimizationReport.Factory.Worker(self.__run_report_factory, self.__parametar_optimizator_factory, run_config_set, mc_set_arr_total, mc_logger)
        
        run_tpl = [(idx,mc_set) for idx,mc_set in enumerate(mc_set_arr)]

        if multi_theads:  
          with concurrent.futures.ProcessPoolExecutor(max_workers=self.workerCount) as executor:
            # Map the do function to the list of tasks
            futures = [executor.submit(worker.do_args, x) for x in run_tpl]
            concurrent.futures.wait(futures)
            new_rr_list = [future.result() for future in futures]
        else:
          new_rr_list = [worker.do_args(tpl) for tpl in run_tpl]
              
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