from dataclasses import dataclass
from datetime import datetime


@dataclass(unsafe_hash=True)
class Deal:
    def __init__(self, open_date: datetime,
                 open_price: float,
                 close_date: datetime,
                 close_price: float,
                 amount: float,
                 commission_open: float = 0,
                 commission_close: float = 0,
                 commission_holding: float = 0):
        if open_price <= 0:
            raise AttributeError("Open price must be > 0", name="open_price")
        if close_price <= 0:
            raise AttributeError("Close price must be > 0", name="close_price")
        if open_date > close_date:
            raise AttributeError(
                "Close date must be > Open date", name="close_date")
        if amount == 0:
            raise AttributeError("Deal must has amount != 0", name="amount")
        if commission_open > 0 or commission_close > 0 or commission_holding > 0:
            raise AttributeError("Commisison must be <= 0")

        self.__open_date: datetime = open_date
        self.__open_price: float = open_price
        self.__close_date: datetime = close_date
        self.__close_price: float = close_price
        self.__amount: float = amount
        self.__commission_open: float = commission_open
        self.__commission_close: float = commission_close
        self.__commission_holding: float = commission_holding

        self.__commission_total = self.commission_open + \
            self.commission_close + self.commission_holding

        self.__result = (self.close_price - self.open_price) * \
            self.amount + self.commission_total

    @property
    def open_date(self) -> datetime:
        return self.__open_date

    @property
    def open_price(self) -> float:
        return self.__open_price

    @property
    def close_date(self) -> datetime:
        return self.__close_date

    @property
    def close_price(self) -> float:
        return self.__close_price

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def commission_open(self) -> float:
        return self.__commission_open

    @property
    def commission_close(self) -> float:
        return self.__commission_close

    @property
    def commission_holding(self) -> float:
        return self.__commission_holding

    @property
    def commission_total(self) -> float:
        return self.__commission_total

    @property
    def result(self) -> float:
        return self.__result
