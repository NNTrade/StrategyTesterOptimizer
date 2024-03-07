from __future__ import annotations
import logging
from venv import logger
from ....simulation.config import StrategyConfig, StrategyId
from ....simulation.models import Deal, SimulationLog
from .data_frame_bar_feed import BarFeed
from pyalgotrade import strategy
from pyalgotrade import logger
from pyalgotrade.bar import Bars
from datetime import datetime
from typing import Dict, List, Callable
import pyalgotrade.broker
from pyalgotrade.broker import backtesting
import pyalgotrade.strategy.position
from pyalgotrade.strategy.position import LongPosition, Position, ShortPosition
from pyalgotrade.broker import OrderExecutionInfo, Order
from .data_frame_bar_feed import CustomValuesWrapper
from pyalgotrade.dataseries.bards import BarDataSeries
from pyalgotrade.bar import BasicBar

class StrategyWrapper(strategy.BaseStrategy):

    class Factory:
        """Factory for building instance of Strategies while simulating
        """
        @staticmethod
        def Single(strategy_id:StrategyId,build_func:Callable[[BarFeed, StrategyConfig],StrategyWrapper])->StrategyWrapper.Factory:
            return StrategyWrapper.Factory({strategy_id: build_func})
        
        def __init__(self, strategy_builder_dict:Dict[StrategyId,Callable[[BarFeed, StrategyConfig],StrategyWrapper]]) -> None:
            self.strategy_builder_dict = strategy_builder_dict
            pass
        def get(self, strategy_id:StrategyId, bf:BarFeed, strategy_cfg:StrategyConfig)->StrategyWrapper:
            return self.strategy_builder_dict[strategy_id](bf,strategy_cfg)
    
    def __init__(self, barFeed:BarFeed, strategy_config: StrategyConfig, cash_or_brk=1000000):
        logger.level = logging.root.level
        if isinstance(cash_or_brk, pyalgotrade.broker.Broker):
            broker:pyalgotrade.broker.Broker = cash_or_brk
        else:
            broker:pyalgotrade.broker.Broker = backtesting.Broker(cash_or_brk, barFeed)
        
        strategy.BaseStrategy.__init__(self, barFeed, broker)
        
        self.__useAdjustedValues = False
        self.setUseEventDateTimeInLogs(True)
        
        self._strategy_config = strategy_config
        self.__cap_log: Dict[datetime, float] = {}
        self.__deal_list: List[Deal] = []
        self.__open_deal_dict:Dict[Position, Deal] = {}

    def _get_custom_value_feed(self, instrument:str, custom_value_name:str)->CustomValuesWrapper:
        """Get custom values as indicator

        Args:
            instrument (str): stock aliase name
            custom_value_name (str): custom value name

        Returns:
            CustomValuesWrapper: custom value in indicator wrapper
        """
        bds:BarDataSeries = self.getFeed()[instrument]
        return CustomValuesWrapper(bds.getExtraDataSeries(custom_value_name))
    
    @property
    def open_deals(self)->List[Deal]:
        return list(self.__open_deal_dict.values())

    @property
    def open_positions(self)->List[Position]:
        return list(self.__open_deal_dict.keys())
    
    def run(self):
        self.__cap_log = {}
        self.__deal_list = []
        super().run()
        return SimulationLog(self.__cap_log, self.__deal_list)
    
    def getUseAdjustedValues(self):
        return self.__useAdjustedValues
    
    def _get_cur_equity(self)->float:
        return self.getBroker().getEquity()
    
    def _action_to_stirng(self, action):
        if action == Order.Action.BUY:
            return "BUY"
        elif action == Order.Action.SELL:
            return "SELL"
        elif action == Order.Action.SELL_SHORT:
            return "SELL_SHORT"
        elif action == Order.Action.BUY_TO_COVER:
            return "BUY_TO_COVER"
        else:
            raise Exception(f"Unexpected action {action}")
        
    def onEnterCanceled(self, position:Position):
        raise Exception("Unexpected call onEnterCanceled")
    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        raise Exception("Unexpected call onExitCanceled")
    
    def onEnterOk(self, position:Position):
        order: Order = position.getEntryOrder() # type: ignore
        execInfo: OrderExecutionInfo = order.getExecutionInfo() # type: ignore
        
        
        deal = Deal.BuildFromCap(execInfo.getDateTime(), execInfo.getPrice(), execInfo.getQuantity(), order.getInstrument(), self._get_cur_equity())
        self.__deal_list.append(deal)
        self.__open_deal_dict[position] = deal
        self.info(f"Open Deal: #{deal.id} direction {deal.direction} at {deal.open_price}")
    
    def onExitOk(self, position:Position):
        order: Order = position.getExitOrder() # type: ignore
        execInfo: OrderExecutionInfo = order.getExecutionInfo() # type: ignore
        deal = self.__open_deal_dict.pop(position)
        deal.close_deal(execInfo.getDateTime(), execInfo.getPrice())
        self.info(f"Close Deal: #{deal.id} direction {deal.direction} at {deal.close_price}. Result {deal.result}")
        
    def setUseAdjustedValues(self, useAdjusted):
        self.getFeed().setUseAdjustedValues(useAdjusted)
        self.getBroker().setUseAdjustedValues(useAdjusted)
        self.__useAdjustedValues = useAdjusted


    def onBars(self, bars:Bars):
        equity = self._get_cur_equity()
        self.__cap_log[bars.getDateTime()] = equity # type: ignore
        self.__cur_bars = bars
        self._onBars(bars)
        
    def _onBars(self, bars:Bars):
        ...

    def enter_long_percent_of_load(self, instrument:str, percent_of_load:float)->LongPosition:
        equity = self._get_cur_equity()
        bar: BasicBar = self.__cur_bars[instrument]        
        return self.enterLong(instrument, equity * percent_of_load / bar.getPrice(), True, True)
    
    def enter_short_percent_of_load(self, instrument:str, percent_of_load:float)->ShortPosition:
        equity = self._get_cur_equity()
        bar: BasicBar = self.__cur_bars[instrument]        
        return self.enterShort(instrument, equity * percent_of_load / bar.getPrice(), True, True)