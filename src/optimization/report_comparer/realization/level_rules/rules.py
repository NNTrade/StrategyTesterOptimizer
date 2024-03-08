from __future__ import annotations
from .....simulation.report.simulation_report import SimulationReport
import numpy as np
from abc import ABC, abstractmethod
from typing import Callable, get_args, List,get_type_hints
from .value_extractors import absValueExtractor

class absRule(ABC):
    @abstractmethod
    def apply(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport], prev_level:float, new_level:float)->float:
        ...
    @staticmethod
    def __check_callable_type(callable_obj):
        # Get the type hints of the callable object
        type_hints = get_type_hints(callable_obj)
        
        # Check if the type hints match the expected type hint
        if callable_obj.__code__.co_argcount == 4 and \
                isinstance(type_hints.get('return'), float) and \
                isinstance(type_hints.get('param1'), list) and \
                isinstance(type_hints.get('param2'), list):
            print("The callable object matches the expected type hint.")
        else:
            print("The callable object does not match the expected type hint.")

    @staticmethod
    def extract_rule_method(value:absRule|type|Callable[[List[SimulationReport],List[SimulationReport],float,float],float])\
                                ->Callable[[List[SimulationReport],List[SimulationReport],float,float],float]:
        if isinstance(value, type):
            assert issubclass(value,absRule), f"Get type {value} which doesn'tinherit from {absRule.__name__}"
            value = value()
            
        if isinstance(value, absRule):
            assert hasattr(value, "apply"), f"Getted {value} doesn't have apply method"
            value = value.apply
        
        assert isinstance(value, Callable), "Unknown type"
        #_ret = get_args(value)
        #input_types, return_type = _ret
        #assert (input_types == [List[SimulationReport],List[SimulationReport],float,float] and return_type == float), f"Function doesn't fit {Callable[[List[SimulationReport],List[SimulationReport],float,float],float]}"
        return value 
    
class ValueRises(absRule):
    def __init__(self, value_extractor: absValueExtractor|type) -> None:
        if isinstance(value_extractor, type):
            assert issubclass(value_extractor,absValueExtractor), f"Get type {value_extractor} which doesn'tinherit from {absValueExtractor.__name__}"
            value_extractor = value_extractor()
        self.__value_extractor = value_extractor
        super().__init__()

    def apply(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport], prev_level:float, new_level:float)->float:
        return self.__value_extractor.extract(new_sim_reps) - self.__value_extractor.extract(prev_sim_reps)
    
class LevelRises(absRule):
    def apply(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport], prev_level:float, new_level:float)->float:
        return new_level - prev_level

class NewMinYieldIsAbove(absRule):
    def __init__(self, above_level:float=0) -> None:
        self.__above_level = above_level
        super().__init__()
    def apply(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport], prev_level:float, new_level:float)->float:
        if min([sr.metrics.capital.strategy_yield_per_year for sr in new_sim_reps]) <= self.__above_level:
            return -1
        else:
            return 0
        

class NewDeviationInLimit(absRule):
    def __init__(self, mult: float=1) -> None:
        self.__mult = 100000000
        self.__dev_mult = mult
        super().__init__()
    
    def _get_default_std_error(self,ypy_arr:List[float])->float:
        return 1/np.sqrt(len(ypy_arr) + 1)
    
    def _get_avg(self, ypy_arr:List[float])->float:
        assert len(ypy_arr) > 0, "No simulation reports getted"
        
        return np.sum(ypy_arr)*self.__mult/len(ypy_arr)
    def _get_deviation(self,ypy_arr:List[float])->float:
        max_val = max(ypy_arr)*self.__mult
        min_val = min(ypy_arr)*self.__mult
        avg_val = self._get_avg(ypy_arr)
        if avg_val is None or avg_val == 0:
            print("avg_val: "+str(avg_val))
        return max([abs(max_val-avg_val), abs(min_val-avg_val)])/avg_val
    def apply(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport], prev_level:float, new_level:float)->float:
        new_ypy_arr = [sr.metrics.capital.strategy_yield_per_year for sr in new_sim_reps]
        base_dev = self._get_default_std_error(new_ypy_arr)

        std_error = base_dev*self.__dev_mult
        new_dev = self._get_deviation(new_ypy_arr)

        if new_dev > std_error:
            return -1
        return 0

class UntillWin(absRule):
    def __init__(self, list_of_fules:List[absRule]) -> None:
        assert len(list_of_fules) > 0, "At least one rule must be setted"
        self.__list_of_fules = list_of_fules
        super().__init__()
    def apply(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport], prev_level:float, new_level:float)->float:
        for rule in self.__list_of_fules:
            result = rule.apply(prev_sim_reps, new_sim_reps, prev_level, new_level)
            if result != 0:
                return result
        return 0
            