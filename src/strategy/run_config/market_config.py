from dataclasses import dataclass
from datetime import date
from typing import Tuple


@dataclass(unsafe_hash=True)
class MarketConfig:

    def __init__(self, stocks: Tuple, from_date: date, untill_date: date) -> None:
        self.__stocks = stocks
        self.__from_date = from_date
        self.__untill_date = untill_date
        pass

    @property
    def stocks(self) -> Tuple:
        return self.__stocks

    @property
    def from_date(self) -> date:
        return self.__from_date

    @property
    def untill_date(self) -> date:
        return self.__untill_date
