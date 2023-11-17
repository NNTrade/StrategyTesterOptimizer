from __future__ import annotations
from datetime import date
from typing import List, Dict
from .stock_config import StockConfig
from NNTrade.common import TimeFrame
from datetime import timedelta

class MarketConfig:
    """Market data configuration
    """
    STOCKS_F = "stocks"
    STEP_TF_F = "step_timeframe"
    FROM_DATE_F = "from_date"
    UNTILL_DATE_F = "untill_date"
    MIN_RELATION = 1/8
    MAX_RELATION = 1/4

    def __init__(self, stocks: List[StockConfig], step_timeframe: TimeFrame, from_date: date, untill_date: date) -> None:
        if from_date >= untill_date:
            raise AttributeError("From date must be less then untill date")
        if len(stocks) < 1:
            raise AttributeError(
                "You must set at least one stock", name="stocks")
        for stock in stocks:
            if stock.timeframe < step_timeframe:
                raise AttributeError("Timeframe of ticker must be LT step timeframe",
                                     name="step_timeframe", obj=step_timeframe)
        self.__stocks = list(sorted(stocks, reverse=True))
        self.__from_date = from_date
        self.__untill_date = untill_date
        self.__step_timeframe = step_timeframe
        pass

    @property
    def stocks(self) -> List[StockConfig]:
        """List of using stock configuration
        """
        return self.__stocks.copy()

    @property
    def step_timeframe(self) -> TimeFrame:
        """Timeframe of bar step
        """
        return self.__step_timeframe

    @property
    def from_date(self) -> date:
        """Starting date
        """
        return self.__from_date

    @property
    def untill_date(self) -> date:
        """End date (excluded from data set)
        """
        return self.__untill_date
    
    @property
    def period_in_days(self)->int:
        """retun delta between fram_date and untill_date in days

        Returns:
            float: days in config
        """
        return (self.__untill_date - self.__from_date).days
    
    @property
    def period_in_years(self)->float:
        """retun delta between fram_date and untill_date in years

        Returns:
            float: years in config
        """
        return self.period_in_days/365

    def split(self, chunks_count: int) -> List[MarketConfig]:
        ts = self.untill_date - self.from_date
        step_ts = timedelta(days=int(ts.days/chunks_count))
        cur_dt = self.from_date
        ret_cfg = []
        for i in range(chunks_count-1):
            new_untill = cur_dt + step_ts
            if new_untill > self.untill_date:
                new_untill = self.untill_date
            ret_cfg.append(MarketConfig(
                self.stocks, self.step_timeframe, cur_dt, new_untill))
            cur_dt = new_untill
        ret_cfg.append(MarketConfig(
            self.stocks, self.step_timeframe, cur_dt, self.untill_date))
        return ret_cfg
                                 
    def to_dict(self) -> Dict:
        return {
            MarketConfig.STOCKS_F: [s.to_dict() for s in self.stocks],
            MarketConfig.STEP_TF_F: self.step_timeframe.short_name(),
            MarketConfig.FROM_DATE_F: self.from_date,
            MarketConfig.UNTILL_DATE_F: self.untill_date
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((tuple(self.stocks), self.step_timeframe, self.from_date, self.untill_date))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MarketConfig):
            return False
        return self.to_dict() == other.to_dict()
