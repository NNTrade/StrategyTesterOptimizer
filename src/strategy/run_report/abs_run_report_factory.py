from __future__ import annotations
from dataclasses import dataclass
from ..run_config import RunConfig,StrategyId
from .run_report import RunReport,datetime,Dict,List,Deal
from .storage.abs_run_report_storage import absRunReportStorage
from abc import ABC, abstractmethod
from typing import Union

class absRunReportFactory(ABC):
    
    @dataclass
    class RunResult:
        abs_capital_log: Dict[datetime, float]
        deal_list: List[Deal]

    """Factory for producing Reports of strategy run by RunConfig
    """

    def __init__(self, report_storage: Union[absRunReportStorage,None] = None) -> None:
        """Constructor

        Args:
            report_storage (Storage, optional): Run report storage. Defaults to None.
        """
        self.__report_storage: Union[absRunReportStorage,None] = report_storage
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
    def _run(self, run_config: RunConfig)->absRunReportFactory.RunResult:
        """Logic which get result of strategy for run config

        Args:
            run_config (RunConfig): run configuration

        Returns:
            absRunReportFactory.RunResult: strategy run result
        """
        ...

    def get(self, run_config: RunConfig) -> RunReport:
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

        return RunReport(self.strategy_id, run_config, result.abs_capital_log, result.deal_list)
