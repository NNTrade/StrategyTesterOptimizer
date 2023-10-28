from __future__ import annotations
from types import MappingProxyType

from .metrics.metric_container import MetricContainer
from ..absStrategy import absStrategy, Dict, datetime, Deal, List


class RunReport:
    # TODO: [FI-83] Описать RunReport
    """Report of strategy run
    """
    @property
    def abs_capital_log(self) -> Dict[datetime, float]:
        """Log of changing capital, init capital set to 1

        Returns:
            Dict[datetime, float]: _description_
        """
        return self.__capital_log

    @property
    def deal_list(self) -> List[Deal]:
        """List of deals

        Returns:
            List[Deal]: deal info
        """
        return self.__deal_list.copy()

    @staticmethod
    def build_from_strategy(strategy: absStrategy) -> RunReport:
        return RunReport(strategy.abs_capital_log, strategy.deal_list)

    def __init__(self, abs_capital_log: Dict[datetime, float], deal_list: List[Deal]) -> None:
        self.__capital_log = MappingProxyType(
            dict(sorted(abs_capital_log.items())))

        if len(self.__capital_log) == 0:
            raise AttributeError(
                "No infarmation about capitol, must be at least one record", name="strategy.abs_capital_log")
        self.__deal_list = deal_list.copy()

        self.__metric_cnt = MetricContainer(
            self.__capital_log, self.__deal_list)
        pass

    @property
    def metrics(self) -> MetricContainer:
        return self.__metric_cnt
