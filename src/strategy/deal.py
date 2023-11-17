from __future__ import annotations
from typing import Dict,Union
from datetime import datetime


class Deal:
    OPEN_DATE_F = "open_date"
    OPEN_PRICE_F = "open_price"
    CLOSE_DATE_F = "close_date"
    CLOSE_PRICE_F = "close_price"
    AMOUNT_F = "amount"
    START_CAP_F = "start_capital"
    COMMISSION_OPEN_F = "commission_open"
    COMMISSION_CLOSE_F = "commission_close"
    COMMISSION_HOLDING_F = "commission_holding"

    class Builder:
        def __init__(self) -> None:
            self.open_date: datetime = None
            self.open_price: float = None
            self.close_date: Union[datetime,None] = None
            self.close_price: float = None
            self.amount: float = None
            self.start_capital: float = None
            self.commission_open: float = 0
            self.commission_close: float = 0
            self.commission_holding: float = 0
            pass

        def set_open_date(self, value) -> Deal.Builder:
            self.open_date = value
            return self

        def set_open_price(self, value) -> Deal.Builder:
            self.open_price = value
            return self

        def set_close_date(self, value) -> Deal.Builder:
            self.close_date = value
            return self

        def set_close_price(self, value) -> Deal.Builder:
            self.close_price = value
            return self

        def set_amount(self, value) -> Deal.Builder:
            self.amount = value
            return self
        
        def set_start_capital(self, value)->Deal.Builder:
            self.start_capital = value
            return self

        def set_commission_open(self, value) -> Deal.Builder:
            self.commission_open = value
            return self

        def set_commission_close(self, value) -> Deal.Builder:
            self.commission_close = value
            return self

        def set_commission_holding(self, value) -> Deal.Builder:
            self.commission_holding = value
            return self

        def build(self) -> Deal:
            return Deal(self.open_date,
                        self.open_price,
                        self.close_date,
                        self.close_price,
                        self.amount,
                        self.start_capital,
                        self.commission_open,
                        self.commission_close,
                        self.commission_holding)

    def __init__(self, open_date: datetime,
                 open_price: float,
                 close_date: Union[datetime,None],
                 close_price: float,
                 amount: float,
                 start_capital: float,
                 commission_open: float = 0,
                 commission_close: float = 0,
                 commission_holding: float = 0):
        if open_price <= 0:
            raise AttributeError("Open price must be > 0", name="open_price")
        if close_price <= 0:
            raise AttributeError("Close price must be > 0", name="close_price")
        if close_date is not None and open_date > close_date:
            raise AttributeError(
                "Close date must be > Open date", name="close_date")
        if amount == 0:
            raise AttributeError("Deal must has amount != 0", name="amount")
        if commission_open > 0 or commission_close > 0 or commission_holding > 0:
            raise AttributeError("Commisison must be <= 0")
        if start_capital == 0:
            raise AttributeError("Start capital must has amount != 0", name="start_capital")
        
        self.__open_date: datetime = open_date
        self.__open_price: float = open_price
        self.__close_date: datetime = close_date
        self.__close_price: float = close_price
        self.__amount: float = amount
        self.__start_capital:float = start_capital
        self.__commission_open: float = commission_open
        self.__commission_close: float = commission_close
        self.__commission_holding: float = commission_holding

        self.__commission_total = self.commission_open + \
            self.commission_close + self.commission_holding

        self.__result = (self.close_price - self.open_price) * \
            self.amount + self.commission_total
        self.__profit = self.__result / self.__start_capital
        self.__is_closed = self.__close_date is not None

    @property
    def start_capital(self)-> float:
        return self.__start_capital

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

    @property
    def profit(self) -> float:
        return self.__profit

    @property
    def is_closed(self) -> bool:
        return self.__is_closed
    def to_dict(self) -> Dict:
        return {
            self.OPEN_DATE_F: self.open_date,
            self.OPEN_PRICE_F: self.open_price,
            self.CLOSE_DATE_F: self.close_date,
            self.CLOSE_PRICE_F: self.close_price,
            self.AMOUNT_F: self.amount,
            self.START_CAP_F: self.start_capital,
            self.COMMISSION_OPEN_F: self.commission_open,
            self.COMMISSION_CLOSE_F: self.commission_close,
            self.COMMISSION_HOLDING_F: self.commission_holding,
        }

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(tuple(self.to_dict().values()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Deal):
            return False
        return self.to_dict() == other.to_dict()

    def __lt__(self, other):
        # Custom less-than comparison for sorting
        key_order = [
            self.OPEN_DATE_F, self.CLOSE_DATE_F, self.AMOUNT_F,
            self.OPEN_PRICE_F, self.CLOSE_PRICE_F,
            self.COMMISSION_OPEN_F, self.COMMISSION_CLOSE_F, self.COMMISSION_HOLDING_F
        ]
        for key in key_order:
            if getattr(self, key) != getattr(other, key):
                return getattr(self, key) > getattr(other, key)
        return False

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return self.__str__()
