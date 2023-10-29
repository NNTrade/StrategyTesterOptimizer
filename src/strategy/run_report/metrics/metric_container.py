from typing import Dict
from datetime import datetime

from .capital_metric import CapitalMetric
from .deal_metric import DealMetric
from ...absStrategy import Deal, List


class MetricContainer:
    CAP_F = "capital"
    DEALS_F = "deals"
    def __init__(self, capital_log: Dict[datetime, float], deal_list: List[Deal]) -> None:
        self.__capital_metric = CapitalMetric(capital_log)
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
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(tuple([self.capital, self.deals]))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MetricContainer):
            return False
        return self.to_dict() == other.to_dict()
