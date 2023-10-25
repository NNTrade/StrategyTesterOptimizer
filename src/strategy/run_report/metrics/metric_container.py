from typing import Dict
from datetime import datetime

from .capital_metric import CapitalMetric
from .deal_metric import DealMetric
from ...absStrategy import Deal, List


class MetricContainer:
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
