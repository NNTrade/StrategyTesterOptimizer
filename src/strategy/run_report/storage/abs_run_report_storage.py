from __future__ import annotations
from typing import Union
from abc import ABC, abstractmethod
from ..run_report import RunReport
from ...run_config.run_config import RunConfig


class absRunReportStorage(ABC):
    """Run report storage client

    Args:
        ABC (_type_): _description_
    """

    def __init__(self, sub_storage: absRunReportStorage = None) -> None:
        self._sub_storage = sub_storage
        pass

    @abstractmethod
    def _try_get(self, run_config: RunConfig) -> Union[RunReport, None]:
        """logic to get report by config

        Args:
            run_config (RunConfig): run config

        Returns:
            Union[RunReport, None]: founded report or None
        """
        ...

    # BUG [FI-87]: try_get method must recive info about strategy and version for searching reports
    def try_get(self, run_config: RunConfig) -> Union[RunReport, None]:
        """Search does report for run config exist in storage

        Args:
            run_config (RunConfig): Run config

        Returns:
            Union[Report, None]: Finded report or None if not found
        """
        report = self._try_get(run_config)
        if report is not None:
            return report

        if self._sub_storage is not None:
            report = self._sub_storage.try_get(run_config)
            if report is not None:
                if not self.try_add(run_config, report):
                    raise Exception(
                        "Cannot copy report from sub storage to current storage")
                return report
        return None

    def try_add(self, run_config: RunConfig, run_report: RunReport) -> bool:
        """add run report for run config

           raise exception if run report exist but has another report

        Args:
            run_config (RunConfig): run configuration
            run_report (RunReport): run report
        """
        try_add_result = self._try_add(run_config, run_report)
        if try_add_result:
            if self._sub_storage is not None:
                self._sub_storage.try_add(run_config, run_report)
        return try_add_result

    @abstractmethod
    def _try_add(self, run_config: RunConfig, run_report: RunReport) -> bool:
        """Logic of try_add

        Args:
            run_config (RunConfig): _description_
            run_report (RunReport): _description_

        Returns:
            bool: _description_
        """
        ...
