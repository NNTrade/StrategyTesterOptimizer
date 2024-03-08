from __future__ import annotations
from .rules import absRule
from .value_extractors import absValueExtractor, AvgYieldPerYearValueExtractor
from ...abs_report_comparer import absReportComparer,SimulationReport,List
from typing import Callable, Dict

class LevelRulesComparer(absReportComparer):
    
    def __init__(self, lower_level: absRule|type|Callable[[List[SimulationReport],List[SimulationReport],float,float],float], 
                       levels: Dict[float, absRule|type|Callable[[List[SimulationReport],List[SimulationReport],float,float],float]], 
                       level_value_extractor:absValueExtractor|type|Callable[[List[SimulationReport]], float] = AvgYieldPerYearValueExtractor) -> None:
        super().__init__(LevelRulesComparer)
        sorted_keys = sorted(levels.keys())
        self.__levels = []
        for key in sorted_keys:
            value = absRule.extract_rule_method(levels[key])
            self.__levels.append((key, value))
        self.__base_rule = absRule.extract_rule_method(lower_level)
        self.__value_extractory = absValueExtractor.extract_value_extract_method(level_value_extractor)
        
    def __apply_rule(self,rule:Callable[[List[SimulationReport],List[SimulationReport],float,float],float],
                          prev_sim_reps:List[SimulationReport], 
                          new_sim_reps:List[SimulationReport], 
                          prev_level_value:float,
                          new_level_value:float)->float:
        compare_result = rule(prev_sim_reps, new_sim_reps, prev_level_value,new_level_value)
        if compare_result != 0:
            if compare_result > 0:
                self._logger.debug(f"New result with level {new_level_value} better prev result with level {prev_level_value}. New WIN.")
            else:
                self._logger.debug(f"New result with level {new_level_value} worst prev result with level {prev_level_value}. Prev WIN.")
        return compare_result
    
    def comparer(self,prev_sim_reps:List[SimulationReport], new_sim_reps:List[SimulationReport])->float:
        prev_level_value = self.__value_extractory(prev_sim_reps)
        new_level_value = self.__value_extractory(new_sim_reps)
        
        rule = self.__base_rule
        for level, std_mult in self.__levels:
            if prev_level_value > level:
                rule = std_mult
            else:
                compare_result = self.__apply_rule(rule,prev_sim_reps, new_sim_reps, prev_level_value,new_level_value)
                if compare_result != 0:                    
                    return compare_result
                rule = std_mult

        compare_result = self.__apply_rule(rule,prev_sim_reps, new_sim_reps, prev_level_value,new_level_value)
        if compare_result == 0:                    
            compare_result = -1
        return compare_result
