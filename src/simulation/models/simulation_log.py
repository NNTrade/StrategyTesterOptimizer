from __future__ import annotations
from dataclasses import dataclass
from typing import Dict,List
from datetime import datetime
from .deal import Deal

@dataclass
class SimulationLog:
    capital_log: Dict[datetime, float]
    deal_list: List[Deal]

    def to_dict(self)->Dict:
        return {
            "capital_log": self.capital_log,
            "deal_list": [d.to_dict() for d in self.deal_list]
        }
    
    #@staticmethod
    #def build_from_dict(use_dict:Dict)->SimulationLog:


    #    SimulationLog(use_dict["capital_log"]