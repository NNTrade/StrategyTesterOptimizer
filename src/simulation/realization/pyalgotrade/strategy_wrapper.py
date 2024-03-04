import logging
from venv import logger
from ....simulation.config import StrategyConfig
from ....simulation.models import Deal, SimulationLog
from pyalgotrade import strategy
from pyalgotrade import logger
from pyalgotrade.barfeed.csvfeed import BarFeed
from datetime import datetime
from typing import Dict, List
import pyalgotrade.broker
from pyalgotrade.broker import backtesting
import pyalgotrade.strategy.position

class PyalgotradeStrategyWrapper(strategy.BaseStrategy):
    def __init__(self, barFeed:BarFeed, strategy_config: StrategyConfig, cash_or_brk=1000000):
        logger.level = logging.root.level
        if isinstance(cash_or_brk, pyalgotrade.broker.Broker):
            broker = cash_or_brk
        else:
            broker = backtesting.Broker(cash_or_brk, barFeed)

        strategy.BaseStrategy.__init__(self, barFeed, broker)

        self.__useAdjustedValues = False
        self.setUseEventDateTimeInLogs(True)
        
        self._strategy_config = strategy_config
        self._cap_log: Dict[datetime, float] = {}
        self._deal_list: List[Deal] = []

    def run(self):
        self._cap_log = {}
        self._deal_list = []
        super().run()
        return SimulationLog(self._cap_log, self._deal_list)
    
    def getUseAdjustedValues(self):
        return self.__useAdjustedValues

    def setUseAdjustedValues(self, useAdjusted):
        self.getFeed().setUseAdjustedValues(useAdjusted)
        self.getBroker().setUseAdjustedValues(useAdjusted)
        self.__useAdjustedValues = useAdjusted