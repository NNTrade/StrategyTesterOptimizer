from __future__ import annotations
from dataclasses import dataclass
from typing import Dict,List
from datetime import datetime
from .deal import Deal
import json

@dataclass
class SimulationLog:
    CAPITAL_LOG_F = "capital_log"
    DEAL_LIST_F = "deal_list"
    capital_log: Dict[datetime, float]
    deal_list: List[Deal]

    def to_dict(self)->Dict:
        return {
            SimulationLog.CAPITAL_LOG_F: self.capital_log,
            SimulationLog.DEAL_LIST_F: [d.to_dict() for d in self.deal_list]
        }
    
    #@staticmethod
    #def build_from_dict(use_dict:Dict)->SimulationLog:


    #    SimulationLog(use_dict["capital_log"]

    def to_json(self):
        cap_log = {dt.isoformat(): value for dt,value in self.capital_log.items()}
        deal_log = [d.to_json() for d in self.deal_list]
        return json.dumps({SimulationLog.CAPITAL_LOG_F: cap_log,
                            SimulationLog.DEAL_LIST_F:deal_log})

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        cap_log = {datetime.fromisoformat(key): value_json for key, value_json in data[SimulationLog.CAPITAL_LOG_F].items()}
        deal_log = [Deal.from_json(d) for d in data[SimulationLog.DEAL_LIST_F]]
        return cls(cap_log, deal_log)