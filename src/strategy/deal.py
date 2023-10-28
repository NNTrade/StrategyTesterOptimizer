from typing import Dict
from datetime import datetime


class Deal:
    OPEN_DATE_F = "open_date"
    OPEN_PRICE_F = "open_price"
    CLOSE_DATE_F = "close_date"
    CLOSE_PRICE_F = "close_price"
    AMOUNT_F = "amount"
    COMMISSION_OPEN_F = "commission_open"
    COMMISSION_CLOSE_F = "commission_close"
    COMMISSION_HOLDING_F = "commission_holding"

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

    def to_dict(self) -> Dict:
        return {
            self.OPEN_DATE_F: self.open_date,
            self.OPEN_PRICE_F: self.open_price,
            self.CLOSE_DATE_F: self.close_date,
            self.CLOSE_PRICE_F: self.close_price,
            self.AMOUNT_F: self.amount,
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
