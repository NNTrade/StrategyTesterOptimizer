from __future__ import annotations
from typing import Dict,Union
from datetime import datetime

class Deal:
    
    OPEN_DATE_F = "open_date"
    OPEN_PRICE_F = "open_price"
    ASSET_F = "asset"
    AMOUNT_F = "amount"
    USING_CAP_F = "using_cap"
    CLOSE_DATE_F = "close_date"
    CLOSE_PRICE_F = "close_price"    
    COMMISSION_OPEN_F = "commission_open"
    COMMISSION_CLOSE_F = "commission_close"
    COMMISSION_HOLDING_F = "commission_holding"
    IS_CLOSED = "is_closed"

    @staticmethod
    def BuildFromCap(open_date: datetime,
                    open_price: float,
                    amount: float,
                    asset: str,
                    using_cap: float,
                    commission_open: float = 0)->Deal:
        return Deal(open_date, open_price, amount, asset, using_cap, commission_open)
    
    def __init__(self, 
                 open_date: datetime,
                 open_price: float,
                 amount: float,
                 asset: str,
                 using_cap: float,
                 commission_open: float = 0):
        self.__close_date: Union[datetime,None] = None
        self.__close_price: Union[float,None] = None
        self.__commission_close: float = 0
        self.__commission_holding: float = 0
        self.__result = None
        self.__profit = None

        if open_price <= 0:
            raise AttributeError("Open price must be > 0", name="open_price")
        
        if amount == 0:
            raise AttributeError("Deal must has amount != 0", name="amount")
        if commission_open > 0:
            raise AttributeError("Commisison open must be <= 0")
        if using_cap <= 0:
            raise AttributeError("Using cap must me > 0")
        
        self.__open_date: datetime = open_date
        self.__open_price: float = open_price
       
        self.__amount: float = amount
        self.__commission_open: float = commission_open

        self.__using_cap:float = using_cap
        self.__asset:str= asset
        

    def __start_cap(self)->float:
        return self.amount * self.open_price / self.__using_cap
    
    def close_deal(self, date:datetime, price:float,commission_close:float = 0)->CloseDeal:
        if date is None or price is None:
            raise AttributeError("Close date and close price must be not none")
        
        if self.open_date >= date:
            raise AttributeError(
                "Close date must be > Open date", name="close_date")
        if price <= 0:
            raise AttributeError("Close price must be > 0", name="close_price")
        
        if self.__close_date is not None:
            raise Exception("Cann't close closed deal")
        
        if commission_close >0:
             raise AttributeError("Commisison close must be <= 0")
        
        self.__close_price = price
        self.__close_date = date
        self.__commission_close = commission_close

        self.__result = (self.__close_price - self.open_price) * \
            self.amount + self.commission_total
        self.__profit = self.__result / self.__start_cap()
        return self # type: ignore

    def add_commision_holding(self, commision:float)->Deal:
        if self.is_closed:
            raise Exception("Cann't add commision to clased deal")
        self.__commission_holding = self.__commission_holding + commision
        return self
    
    @property
    def open_date(self) -> datetime:
        return self.__open_date

    @property
    def open_price(self) -> float:
        return self.__open_price

    @property
    def close_date(self) -> Union[datetime,None]:
        return self.__close_date

    @property
    def close_price(self) -> Union[float,None]:
        return self.__close_price

    @property
    def amount(self) -> float:
        return self.__amount
    
    @property
    def asset(self)->str:
        return self.__asset
    
    @property
    def using_cap(self)->float:
        return self.__using_cap
    
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
        return self.commission_open + self.commission_close + self.commission_holding

    @property
    def result(self) -> Union[float,None]:
        return self.__result

    @property
    def profit(self) -> Union[float,None]:
        return self.__profit

    @property
    def is_closed(self) -> bool:
        return self.__close_date is not None
    
    @property
    def as_closed(self)->CloseDeal:
        if not self.is_closed:
            raise Exception("Cann't convert opened deal as closed deal")
        return self # type: ignore
    
    def to_dict(self) -> Dict:
        return {
            self.OPEN_DATE_F: self.open_date,
            self.OPEN_PRICE_F: self.open_price,
            self.AMOUNT_F: self.amount,
            self.ASSET_F: self.asset,
            self.USING_CAP_F: self.using_cap,
            self.CLOSE_DATE_F: self.close_date,
            self.CLOSE_PRICE_F: self.close_price,
            self.COMMISSION_OPEN_F: self.__commission_open,            
            self.COMMISSION_HOLDING_F: self.__commission_holding,
            self.COMMISSION_CLOSE_F: self.__commission_close,
            self.IS_CLOSED: int(self.is_closed)
        }

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(tuple(self.to_dict().items()))

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

class CloseDeal(Deal):
    @property
    def close_date(self) -> datetime:
        return super().close_date# type: ignore

    @property
    def close_price(self) -> float:
        return super().close_price# type: ignore
    
    @property
    def result(self) -> float:
        return super().result# type: ignore

    @property
    def profit(self) -> float:
        return super().profit# type: ignore