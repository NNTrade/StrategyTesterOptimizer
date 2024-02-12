from __future__ import annotations

from .report.simulation_report import SimulationReport
from .config import SimulationConfig,StrategyId
from .storage.abs_simulation_log_storage import absSimulationLogStorage
from abc import ABC, abstractmethod
from typing import Union
from .models import SimulationLog

class absTradingSimulatior(ABC):
    """Abstract trading simulation factory

    Args:
        ABC (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    def __init__(self, report_storage: Union[absSimulationLogStorage,None] = None) -> None:
        """Constructor

        Args:
            report_storage (Storage, optional): Run report storage. Defaults to None.
        """
        self.__log_storage: Union[absSimulationLogStorage,None] = report_storage
        pass
    
    @property
    @abstractmethod
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
        if self.__log_storage is not None:
            sl = self.__log_storage.try_get(self.strategy_id, run_config)
            if sl is not None:
                return sl
            
        sl = self._run(run_config)

        if self.__log_storage is not None:
          self.__log_storage.try_add(self.strategy_id, run_config,sl)  
        
        return sl
    
    def get_report(self, simulation_config: SimulationConfig) -> SimulationReport: 
        sl = self.get_log(simulation_config)
        return SimulationReport(self.strategy_id, simulation_config, sl)