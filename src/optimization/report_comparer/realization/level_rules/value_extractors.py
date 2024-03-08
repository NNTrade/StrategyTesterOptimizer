from __future__ import annotations
from .....simulation.report.simulation_report import SimulationReport
import numpy as np
from abc import ABC, abstractmethod
from typing import Callable, ValuesView, get_args, List

class absValueExtractor(ABC):
    @abstractmethod
    def extract(self,sim_reps:List[SimulationReport])->float:
        ...
    
    @staticmethod
    def extract_value_extract_method(value:absValueExtractor|type|Callable[[List[SimulationReport]], float])->Callable[[List[SimulationReport]], float]:
        if isinstance(value, type):
            assert issubclass(value, absValueExtractor), f"Get type {value} which doesn'tinherit from {absValueExtractor.__name__}"
            value = value()

        if isinstance(value, absValueExtractor):
            assert hasattr(value, "extract"), f"Getted {value} doesn't have apply method"
            value = value.extract
                
        assert isinstance(value, Callable), "Unknown type"
        #input_types, return_type = get_args(value)

        #assert (input_types == [List[SimulationReport]] and return_type == float), f"Function doesn't fit {Callable[[List[SimulationReport]], float]}"
        return value

class AvgYieldPerYearValueExtractor(absValueExtractor):
    def extract(self,sim_reps:List[SimulationReport])->float:
        assert len(sim_reps) > 0
        return np.sum([sr.metrics.capital.strategy_yield_per_year for sr in sim_reps])/len(sim_reps)

class MaxYieldPerYearValueExtractor(absValueExtractor):
    def extract(self,sim_reps:List[SimulationReport])->float:
        assert len(sim_reps) > 0
        return max([sr.metrics.capital.strategy_yield_per_year for sr in sim_reps])

class MinYieldPerYearValueExtractor(absValueExtractor):
    def extract(self,sim_reps:List[SimulationReport])->float:
        assert len(sim_reps) > 0
        return min([sr.metrics.capital.strategy_yield_per_year for sr in sim_reps])