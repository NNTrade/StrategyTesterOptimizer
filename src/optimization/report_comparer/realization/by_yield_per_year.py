from __future__ import annotations
from enum import Enum
from ..abs_report_comparer import absReportComparer,SimulationReport,List
import numpy as np

class ByYieldPerYear(absReportComparer):
    class getType(Enum):
        avg=0,
        max=1,
        min=-1
    def __init__(self,get_type:ByYieldPerYear.getType = getType.avg) -> None:
        self.__mult = 100000000
        self.__get_type = get_type
        super().__init__("ByYieldPerYear")

    def _get(self, sim_reps:List[SimulationReport])->float:
        assert len(sim_reps) > 0, "No simulation reports getted"
            
        if self.__get_type == ByYieldPerYear.getType.avg:
            return np.sum([sr.metrics.capital.strategy_yield_per_year for sr in sim_reps])/len(sim_reps)
        elif self.__get_type == ByYieldPerYear.getType.max:
            return np.max([sr.metrics.capital.strategy_yield_per_year for sr in sim_reps])
        elif self.__get_type == ByYieldPerYear.getType.min:
            return np.min([sr.metrics.capital.strategy_yield_per_year for sr in sim_reps])
        
        raise Exception("Unexpected get type")

    def comparer(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport])->int:
        new_str_yield_per_year = self._get(new_sim_reps)
        prev_str_yield_per_year = self._get(prev_sim_reps)
        compare_result = int((new_str_yield_per_year - prev_str_yield_per_year)*self.__mult)
        if compare_result > 0:
            self._logger.debug(f"New result {new_str_yield_per_year} > {prev_str_yield_per_year}. Compare result {compare_result/self.__mult}")
        else:
            self._logger.debug(f"New result {new_str_yield_per_year} < {prev_str_yield_per_year}. Compare result {compare_result/self.__mult}")
        return compare_result
        
