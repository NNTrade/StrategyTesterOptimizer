from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass(unsafe_hash=True)
class MarketConfig:

    def __init__(self, stocks: List, from_date: date, untill_date: date) -> None:
        if from_date >= untill_date:
            raise AttributeError("From date must be less then untill date")
        if len(stocks) < 1:
            raise AttributeError(
                "You must set at least one stock", name="stocks")
        self.__stocks = list(stocks)
        self.__from_date = from_date
        self.__untill_date = untill_date
        pass

    @property
    def stocks(self) -> List:
        return self.__stocks.copy()

    @property
    def from_date(self) -> date:
        return self.__from_date

    @property
    def untill_date(self) -> date:
        return self.__untill_date
