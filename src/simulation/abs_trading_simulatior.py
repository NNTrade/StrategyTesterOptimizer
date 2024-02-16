from __future__ import annotations
import logging
from .report.simulation_report import SimulationReport
from .config import SimulationConfig,StrategyId
from .cache.abs_simulation_log_storage import absSimulationLogStorage
from abc import ABC, abstractmethod, abstractproperty
from typing import Union
from .models import SimulationLog
import pprint

class absTradingSimulatior(ABC):
    """Abstract trading simulation factory

    Args:
        ABC (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    def __init__(self, report_storage: Union[absSimulationLogStorage,None] = None, trading_sim_name:Union[str,None]= None) -> None:
        """Constructor

        Args:
            report_storage (Storage, optional): Run report storage. Defaults to None.
        """
        self.__log_cache: Union[absSimulationLogStorage,None] = report_storage
        self.__logger = logging.getLogger(f"absTradingSimulatior[{self.strategy_id}]")
        self._logger = self.__logger if trading_sim_name is None else self.__logger.getChild(trading_sim_name)
        pass
    
    @abstractproperty
    def strategy_id(self)->StrategyId:
        """Strategy id which work in this factory

        Returns:
            StrategyId: strategy id
        """
        ...
    
    @abstractmethod
    def _run(self, run_config: SimulationConfig)->SimulationLog:
        """Logic which get result of strategy for run config

        Args:
            run_config (RunConfig): run configuration

        Returns:
            absRunReportFactory.RunResult: strategy run result
        """
        ...

    def get_log(self, run_config: SimulationConfig) -> SimulationLog:
        """get Strategy run report by run configuration

        Args:
            run_config (RunConfig): run configuration

        Returns:
            StrategyReport: Strategy run report
        """
        self.__logger.info(f"Getting log of:\n{run_config}")

        if self.__log_cache is not None:
            self.__logger.info("Try find log in store")
            sl = self.__log_cache.try_get(self.strategy_id, run_config)
            if sl is not None:
                return sl
        
        self.__logger.info(f"No cache source or chache not found. Star simulation")
        sl = self._run(run_config)

        if self.__log_cache is not None:
          self.__logger.info("Add log to store")
          self.__log_cache.try_add(self.strategy_id, run_config,sl)  
        
        return sl
    
    def get_report(self, simulation_config: SimulationConfig) -> SimulationReport: 
        self.__logger.info(f"Getting report of\n{simulation_config}")
        sl = self.get_log(simulation_config)

        self.__logger.info("Convert log into report")
        report = SimulationReport(self.strategy_id, simulation_config, sl)
        self.__logger.info(f"Simulation report metric:\n{report.metrics}")
        return report