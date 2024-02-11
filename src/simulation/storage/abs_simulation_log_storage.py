from __future__ import annotations
from typing import Union
from abc import ABC, abstractmethod

from src.simulation.config.simulation_config import SimulationConfig
from ..models import SimulationLog
from ..config import SimulationConfig,StrategyId


class absSimulationLogStorage(ABC):
    """Run report storage client

    Args:
        ABC (_type_): _description_
    """

    def __init__(self, sub_storage: Union[absSimulationLogStorage,None] = None) -> None:
        self._sub_storage = sub_storage
        pass

    @abstractmethod
    def _try_get(self, strategy_id: StrategyId, simulation_config: SimulationConfig) -> Union[SimulationLog, None]:
        """logic to get report by config

        Args:
            simulation_config (SimulationConfig): simulation run config

        Returns:
            Union[RunReport, None]: founded report or None
        """
        ...

    def try_get(self, strategy_id: StrategyId, simulation_config: SimulationConfig) -> Union[SimulationLog, None]:
        """Search does report for run config exist in storage

        Args:
            simulation_config (SimulationConfig): simulation run config

        Returns:
            Union[SimulationLog, None]: Finded report or None if not found
        """
        report = self._try_get(strategy_id,simulation_config)
        if report is not None:
            return report

        if self._sub_storage is not None:
            report = self._sub_storage.try_get(strategy_id, simulation_config)
            if report is not None:
                if not self.try_add(strategy_id,simulation_config, report):
                    raise Exception(
                        "Cannot copy report from sub storage to current storage")
                return report
        return None

    def try_add(self, strategy_id:StrategyId, simulation_config: SimulationConfig, simulation_report: SimulationLog) -> bool:
        """add run report for run config

           raise exception if run report exist but has another report

        Args:
            simulation_config (SimulationConfig): run configuration
            simulation_report (SimulationLog): run report
        """
        try_add_result = self._try_add(strategy_id,simulation_config, simulation_report)
        if try_add_result:
            if self._sub_storage is not None:
                self._sub_storage.try_add(strategy_id,simulation_config, simulation_report)
        return try_add_result

    @abstractmethod
    def _try_add(self, strategy_id:StrategyId, simulation_config: SimulationConfig, simulation_report: SimulationLog) -> bool:
        """Logic of try_add

        Args:
            simulation_config (SimulationConfig): _description_
            simulation_report (SimulationLog): _description_

        Returns:
            bool: _description_
        """
        ...
