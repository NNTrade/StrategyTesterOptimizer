from abc import ABC
import logging
from typing import List

from ...simulation.report.simulation_report import SimulationReport


class absReportComparer(ABC):
    def __init__(self, comparer:str|type|None=None) -> None:
        self._logger = logging.getLogger("absReportComparer")
        if comparer is not None:
            if isinstance(comparer, str):
                comparer_name = comparer
            elif isinstance(comparer, type):
                comparer_name = comparer.__name__
            else:
                raise AttributeError("Wrong type of comparer parameter", "comparer", comparer)
            
            self._logger = self._logger.getChild(comparer_name)
        super().__init__()

    def comparer(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport])->int:
        ...