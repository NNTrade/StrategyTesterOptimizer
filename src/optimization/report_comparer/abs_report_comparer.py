from abc import ABC
import logging
from typing import Union

from ...simulation.report.simulation_report import SimulationReport


class absReportComparer(ABC):
    def __init__(self, comparer_name:Union[str,None]=None) -> None:
        self._logger = logging.getLogger("absReportComparer")
        if comparer_name is not None:
            self._logger = self._logger.getChild(comparer_name)
        super().__init__()

    def comparer(self,prev:SimulationReport, new: SimulationReport)->int:
        ...