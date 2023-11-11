from __future__ import annotations
import math
from types import MappingProxyType

from .metrics.metric_container import MetricContainer
from ..absStrategy import absStrategy, Dict, datetime, Deal, List
from ..run_config import RunConfig

class RunReport:
    RUN_CONFIG_F = "run_config"
    METRIC_F = "metric"
    ABS_CAP_LOG_F = "abs_cap_log"
    DEAL_LIST_F = "deal_list"
    """Report of strategy run
    """
    @property
    def abs_capital_log(self) -> Dict[datetime, float]:
        """Log of changing capital, init capital set to 1

        Returns:
            Dict[datetime, float]: _description_
        """
        return self.__capital_log.copy()

    @property
    def deal_list(self) -> List[Deal]:
        """List of deals

        Returns:
            List[Deal]: deal info
        """
        return self.__deal_list.copy()

    @staticmethod
    def build_from_strategy(run_config: RunConfig, strategy: absStrategy) -> RunReport:
        return RunReport(run_config, strategy.abs_capital_log, strategy.deal_list)

    def __init__(self, run_config: RunConfig, abs_capital_log: Dict[datetime, float], deal_list: List[Deal]) -> None:
        self.__capital_log = dict(sorted(abs_capital_log.items()))

        if len(self.__capital_log) == 0:
            raise AttributeError(
                "No infarmation about capitol, must be at least one record", name="strategy.abs_capital_log")
        self.__deal_list = sorted(deal_list.copy())

        self.__metric_cnt = MetricContainer(run_config.market_cfg,
            self.__capital_log, self.__deal_list)
        self.__run_cfg = run_config
        pass

    @property
    def metrics(self) -> MetricContainer:
        return self.__metric_cnt

    @property
    def run_config(self) -> RunConfig:
        return self.__run_cfg

    def to_dict(self) -> Dict:
        return {
            RunReport.RUN_CONFIG_F: self.run_config.to_dict(),
            RunReport.METRIC_F: self.metrics.to_dict(),
            RunReport.ABS_CAP_LOG_F: self.abs_capital_log,
            RunReport.DEAL_LIST_F: [d.to_dict() for d in self.deal_list]
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(self.run_config) * hash(self.metrics) * math.prod([hash(d) for d in self.deal_list]) * hash(frozenset(self.abs_capital_log))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RunReport):
            return False
        return self.to_dict() == other.to_dict()
