from __future__ import annotations
import math
from .metrics.metric_container import MetricContainer,Dict,datetime
from ..config import SimulationConfig,StrategyId
from typing import List
from ..models.deal import Deal

class SimulationReport:
    STRATEGY_ID_F = "strategy_id"
    RUN_CONFIG_F = "run_config"
    METRIC_F = "metric"
    ABS_CAP_LOG_F = "abs_cap_log"
    DEAL_LIST_F = "deal_list"
    """Report of strategy run
    """
    @property
    def capital_log(self) -> Dict[datetime, float]:
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


    def __init__(self, strategy_id: StrategyId, run_config: SimulationConfig, abs_capital_log: Dict[datetime, float], deal_list: List[Deal]) -> None:
        if len(abs_capital_log) == 0:
            raise AttributeError(
                "No infarmation about capitol, must be at least one record", name="abs_capital_log")
        
        first_cap_log = min(abs_capital_log.keys()).date()
        if first_cap_log < run_config.market_cfg.from_date:
            raise AttributeError(f"Given capital log to run report starts ({first_cap_log}) out of border of market config {run_config.market_cfg.from_date}", name="abs_capital_log")
        last_cap_log = max(abs_capital_log.keys()).date()
        if last_cap_log >= run_config.market_cfg.untill_date:
            raise AttributeError(f"Given capital log to run report ends ({last_cap_log}) out of border of market config {run_config.market_cfg.untill_date}", name="abs_capital_log")
        
        if len(deal_list) > 0 :
            first_deal_dt = min([d.open_date for d in deal_list]).date()
            if first_deal_dt < run_config.market_cfg.from_date:
                raise AttributeError(f"Given deals log has deals started ({first_deal_dt}) out of border of market config {run_config.market_cfg.from_date}", name="deal_list")
            
            last_deal_dt = max([first_deal_dt,*[d.close_date.date() for d in deal_list if d.close_date is not None]])
            if last_deal_dt >= run_config.market_cfg.untill_date:
                raise AttributeError(f"Given deals log has deals ended ({last_deal_dt}) out of border of market config {run_config.market_cfg.untill_date}", name="deal_list")

        self.__capital_log = dict(sorted(abs_capital_log.items()))

        
        self.__deal_list = sorted(deal_list.copy())

        self.__metric_cnt = MetricContainer(run_config.market_cfg,
            self.__capital_log, self.__deal_list)
        self.__run_cfg = run_config
        self.__str_id = strategy_id
        pass

    @property
    def strategy_id(self)->StrategyId:
        return self.__str_id
    
    @property
    def metrics(self) -> MetricContainer:
        return self.__metric_cnt

    @property
    def simulation_config(self) -> SimulationConfig:
        return self.__run_cfg

    def to_dict(self) -> Dict:
        return {
            SimulationReport.STRATEGY_ID_F: self.strategy_id.to_dict(),
            SimulationReport.RUN_CONFIG_F: self.simulation_config.to_dict(),
            SimulationReport.METRIC_F: self.metrics.to_dict(),
            SimulationReport.ABS_CAP_LOG_F: self.capital_log,
            SimulationReport.DEAL_LIST_F: [d.to_dict() for d in self.deal_list]
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(self.strategy_id) * hash(self.simulation_config) * hash(self.metrics) * math.prod([hash(d) for d in self.deal_list]) * hash(frozenset(self.capital_log))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimulationReport):
            return False
        return self.to_dict() == other.to_dict()
