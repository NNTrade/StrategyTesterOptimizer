from ....simulation.config import StrategyConfig
from ....simulation.models import Deal, SimulationLog
from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import BarFeed
from datetime import datetime
from typing import Dict, List


class PyalgotradeStrategyWrapper(strategy.BacktestingStrategy):
    def __init__(self, barFeed:BarFeed, strategy_config: StrategyConfig, cash_or_brk=1000000):
        super().__init__(barFeed, cash_or_brk)
        self._strategy_config = strategy_config
        self._cap_log: Dict[datetime, float] = {}
        self._deal_list: List[Deal] = []

    def run(self):
        self._cap_log = {}
        self._deal_list = []
        super().run()
        return SimulationLog(self._cap_log, self._deal_list)