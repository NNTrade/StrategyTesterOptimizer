from __future__ import annotations
from dataclasses import dataclass
from typing import Dict,List
from datetime import datetime
from .deal import Deal

@dataclass
class SimulationLog:
    abs_capital_log: Dict[datetime, float]
    deal_list: List[Deal]