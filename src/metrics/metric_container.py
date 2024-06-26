from __future__ import annotations
from typing import Dict,List
from datetime import datetime
from ..models.simulation_log import SimulationLog
from .capital_metric import CapitalMetric,DatePeriod
from .deal_metric import DealMetric,Deal
import pprint

class MetricContainer:
    CAP_F = "capital"
    DEALS_F = "deals"
    
    @staticmethod
    def build_by_log(simulation_log: SimulationLog)->MetricContainer:
        start_dt = min(simulation_log.capital_log.keys())
        end_dt = max(simulation_log.capital_log.keys())
        dp = DatePeriod(start_dt,end_dt)
        return MetricContainer(dp, simulation_log.capital_log, simulation_log.deal_list)
    
    def __init__(self, date_period_cfg: DatePeriod,capital_log: Dict[datetime, float], deal_list: List[Deal]) -> None:
        self.__capital_metric = CapitalMetric(date_period_cfg, capital_log,deal_list)
        self.__deal_meatric = DealMetric(deal_list)
        pass

    @property
    def capital(self) -> CapitalMetric:
        return self.__capital_metric

    @property
    def deals(self) -> DealMetric:
        return self.__deal_meatric

    def to_dict(self) -> Dict:
        return {
            MetricContainer.CAP_F: self.capital.to_dict(),
            MetricContainer.DEALS_F: self.deals.to_dict()
        }

    def __str__(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(tuple([self.capital, self.deals]))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MetricContainer):
            return False
        return self.to_dict() == other.to_dict()
