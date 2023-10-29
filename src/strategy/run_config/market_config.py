from dataclasses import dataclass
from datetime import date
from typing import List, Dict
from .stock_config import StockConfig
from NNTrade.common import TimeFrame


class MarketConfig:
    STOCKS_F = "stocks"
    STEP_TF_F = "step_timeframe"
    FROM_DATE_F = "from_date"
    UNTILL_DATE_F = "untill_date"

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
        return self.__stocks.copy()

    @property
    def step_timeframe(self) -> TimeFrame:
        return self.__step_timeframe

    @property
    def from_date(self) -> date:
        return self.__from_date

    @property
    def untill_date(self) -> date:
        return self.__untill_date

    def to_dict(self) -> Dict:
        return {
            MarketConfig.STOCKS_F: self.stocks,
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
