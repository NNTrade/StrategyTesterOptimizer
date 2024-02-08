from __future__ import annotations
from .config import SimulationConfig,StrategyId
from .storage.abs_simulation_report_storage import absSimulationReportStorage
from abc import ABC, abstractmethod
from typing import Union
from .models import SimulationLog,SimulationReport

class absTradingSimulationFactory(ABC):
    """Abstract trading simulation factory

    Args:
        ABC (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    def __init__(self, report_storage: Union[absSimulationReportStorage,None] = None) -> None:
        """Constructor

        Args:
            report_storage (Storage, optional): Run report storage. Defaults to None.
        """
        self.__report_storage: Union[absSimulationReportStorage,None] = report_storage
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

    def get(self, run_config: SimulationConfig) -> SimulationReport:
        """get Strategy run report by run configuration

        Args:
            run_config (RunConfig): run configuration

        Returns:
            StrategyReport: Strategy run report
        """
        if self.__report_storage is not None:
            rr = self.__report_storage.try_get(self.strategy_id, run_config)
            if rr is not None:
                return rr
            
        result = self._run(run_config)


        sr = SimulationReport(self.strategy_id, run_config, result.abs_capital_log, result.deal_list)

        if self.__report_storage is not None:
          self.__report_storage.try_add(self.strategy_id, run_config,sr)  
        
        return sr
