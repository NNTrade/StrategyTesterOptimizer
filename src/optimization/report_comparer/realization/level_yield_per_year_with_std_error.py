from __future__ import annotations
from audioop import avg
from enum import Enum
from ..abs_report_comparer import absReportComparer,SimulationReport,List
import numpy as np
from typing import Tuple
DEFAULT_CONFIG = [
        (0, 3),
        (0.04, 2),
        (0.05, 1),
        (0.06, 0.5),
    ]

class LevelYieldPerYearWithStdError(absReportComparer):
    
    def __init__(self, levels: List[Tuple[float, float]] = DEFAULT_CONFIG) -> None:
        self.__mult = 100000000
        self.__levels = sorted(levels, key=lambda x: x[0])
        assert self.__levels[0][0] >=0
        super().__init__(LevelYieldPerYearWithStdError)

    def _get_deviation(self,ypy_arr:List[float])->float:
        max_val = max(ypy_arr)*self.__mult
        min_val = min(ypy_arr)*self.__mult
        avg_val = self._get_avg(ypy_arr)

        return max([abs(max_val-avg_val), abs(min_val-avg_val)])/avg_val

    def _get_default_std_error(self,ypy_arr:List[float])->float:
        return 1/np.sqrt(len(ypy_arr) + 1)
    
    def _get_avg(self, ypy_arr:List[float])->float:
        assert len(ypy_arr) > 0, "No simulation reports getted"
        
        return np.sum(ypy_arr)/len(ypy_arr)*self.__mult

    def comparer(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport])->float:
        prev_ypy = [sr.metrics.capital.strategy_yield_per_year for sr in prev_sim_reps]
        new_ypy = [sr.metrics.capital.strategy_yield_per_year for sr in new_sim_reps]
        avg_prev_str_yield_per_year = self._get_avg(prev_ypy)
        avg_new_str_yield_per_year = self._get_avg(new_ypy)

        if avg_new_str_yield_per_year < avg_prev_str_yield_per_year:
            self._logger.debug(f"New avg_new_str_yield_per_year {avg_new_str_yield_per_year} < avg_prev_str_yield_per_year {avg_prev_str_yield_per_year}. Prev WIN.")
            return -1
        
        cur_std_mult:float|None = None
        for level, std_mult in self.__levels:
            if avg_prev_str_yield_per_year > level:
                cur_std_mult = std_mult
            else:
                break

        if cur_std_mult is not None:
            std_error = self._get_default_std_error(new_ypy) * cur_std_mult
            new_dev = self._get_deviation(new_ypy)

            if new_dev > std_error:
                self._logger.debug(f"New deviation {new_dev} < allowed {std_error}. Prev WIN.")
                return -1
        

        compare_result = int((avg_new_str_yield_per_year - avg_prev_str_yield_per_year))
        if compare_result > 0:
            self._logger.debug(f"New result {avg_new_str_yield_per_year} > {avg_prev_str_yield_per_year}. New WIN. Compare result {compare_result/self.__mult}")
        else:
            self._logger.debug(f"New result {avg_new_str_yield_per_year} < {avg_prev_str_yield_per_year}. Prev WIN. Compare result {compare_result/self.__mult}")
        return compare_result

