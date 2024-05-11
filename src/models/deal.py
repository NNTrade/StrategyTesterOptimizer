from __future__ import annotations
from typing import Dict, Union
from datetime import datetime
import json
from ..common.exceptions import ClosedDealException
import logging

W_001 = True # using_cap > open_price * amount
W_002 = True # close_date == open_date
E_002 = False # close_date == open_date

class Deal:
    G_COUNTER = 0
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
                    commission_open: float = 0) -> Deal:
        return Deal(open_date, open_price, amount, asset, using_cap, commission_open)

    def __init__(self,
                 open_date: datetime,
                 open_price: float,
                 amount: float,
                 asset: str,
                 using_capital: float,
                 commission_open: float = 0):
        Deal.G_COUNTER = Deal.G_COUNTER + 1
        self.__id = Deal.G_COUNTER
        self.__close_date: Union[datetime, None] = None
        self.__last_price: float = open_price
        self.__commission_close: float = 0
        self.__commission_holding: float = 0

        if open_price <= 0:
            raise AttributeError("Open price must be > 0", name="open_price")

        if amount == 0:
            raise AttributeError("Deal must has amount != 0", name="amount")
        if commission_open > 0:
            raise AttributeError("Commisison open must be <= 0")
        if using_capital <= 0:
            raise AttributeError("Using cap must me > 0")
        
        self.__open_date: datetime = open_date
        self.__open_price: float = open_price

        self.__amount: float = amount
        self.__commission_open: float = commission_open
        
        self.__using_cap: float = using_capital
        self.__asset: str = asset
        self.__update_profit_and_interest()
        self.__logger = logging.getLogger(f"Deal({asset})_{open_date.strftime('%Y%m%d%H%M%S')}")
        
        if W_001 and using_capital > open_price * amount:
            self.__logger.warning("using_capital (%f) > open_price (%f) * amount (%f)", using_capital,open_price,amount )

    @property
    def id(self) -> int:
        return self.__id

    def set_last_price(self, price: float) -> Deal:
        if self.is_closed:
            raise Exception("Cann't set last price for closed deal")

        self.__last_price = price
        self.__update_profit_and_interest()
        return self

    def close_deal(self, date: datetime, price: float, commission_close: float = 0) -> CloseDeal:
        """Close deal

        Args:
            date (datetime): date of closing
            price (float): close price
            commission_close (float, optional): commision of closing. Defaults to 0.

        Raises:
            AttributeError: errors in input attributes
            ClosedDealException: operation forbidden for closed deals. Deal has been already closed

        Returns:
            CloseDeal: Deal with addition typing attributes
        """
        if date is None or price is None:
            raise AttributeError("Close date and close price must be not none")

        if self.open_date > date:
            raise AttributeError(
                "Close date must be > Open date", name="close_date")
        if self.open_date == date:
            if E_002:
                raise AttributeError(
                    f"Close date must be >= Open date. This is optional Exception configured by E_002 parameter", name="close_date")
            elif W_002:
                self.__logger.warning("Closed date == Opened date")

        if price <= 0:
            raise AttributeError("Close price must be > 0", name="close_price")

        if self.is_closed:
            raise ClosedDealException("Cann't close closed deal")

        if commission_close > 0:
             raise AttributeError("Commisison close must be <= 0")
        
        self.__last_price = price
        self.__close_date = date
        self.__commission_close = commission_close

        self.__update_profit_and_interest()
        return self  # type: ignore

    def __update_profit_and_interest(self):
        self.__profit = (self.__last_price - self.open_price) * \
            self.amount + self.commission_total
        self.__interest = self.__profit / self.__using_cap  # type: ignore

    def add_commision_holding(self, commision: float) -> Deal:
        """Add commision for deal

        Args:
            commision (float): amount of commision

        Raises:
            Exception: Deal is closed

        Returns:
            Deal: self instance
        """
        if self.is_closed:
            raise Exception("Cann't add commision to clased deal")
        self.__commission_holding = self.__commission_holding + commision
        self.__update_profit_and_interest()
        return self

    @property
    def is_long(self) -> bool:
        return self.amount > 0

    @property
    def is_short(self) -> bool:
        return self.amount < 0

    @property
    def direction(self) -> str:
        """Text description Long or Short

        Returns:
            str: text description
        """
        return "Long" if self.is_long else "Short"

    @property
    def direction_mult(self) -> int:
        """direction as multiplication value\n
            1  - Long\n
            -1 - Short

        Returns:
            int: multipclication direction aliase
        """
        return 1 if self.is_long else -1

    @property
    def open_date(self) -> datetime:
        return self.__open_date

    @property
    def open_price(self) -> float:
        return self.__open_price

    @property
    def close_date(self) -> Union[datetime, None]:
        """Close date, if deal is not Closed than None
        """
        return self.__close_date

    @property
    def close_price(self) -> Union[float, None]:
        """Close price, if deal is not Closed than None
        """
        return self.__last_price

    @property
    def amount(self) -> float:
        """amount of asset in deal. Positive is Long, Negative is short

        Returns:
            float: _description_
        """
        return self.__amount
    
    @property
    def amount_abs(self) -> float:
        """absolute value of asset amount in deal. 

        Returns:
            float: _description_
        """
        return abs(self.__amount)
    
    @property
    def asset(self)->str:
        """Asset Name
        """
        return self.__asset
    
    @property
    def using_capital(self)->float:
        """Using capital for deal. If you use leverage it could be less than asset * open_price

        Returns:
            float: _description_
        """
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
    def profit(self) -> float:
        """Result amount of cash gained or loss by deal.\n
        profit = (open_price - close_price) * amount - commision_total 
        """
        return self.__profit

    @property
    def interest(self) -> float:
        """Percent gained from deal.\n
        interest = profit / using_capital
        """
        return self.__interest

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
            self.USING_CAP_F: self.using_capital,
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
    
    def to_json(self):
        json_dic = {
            Deal.OPEN_DATE_F: self.open_date.isoformat(),
            Deal.OPEN_PRICE_F: self.open_price,
            Deal.AMOUNT_F: self.amount,
            Deal.ASSET_F: self.asset,
            Deal.USING_CAP_F: self.using_capital,
            Deal.COMMISSION_OPEN_F: self.commission_open,
            Deal.COMMISSION_HOLDING_F: self.commission_holding,
            Deal.IS_CLOSED : int(self.is_closed)
        }
        if self.is_closed:
            closed_self = self.as_closed            
            json_dic[Deal.CLOSE_DATE_F] = closed_self.close_date.isoformat()
            json_dic[Deal.CLOSE_PRICE_F] = closed_self.close_price            
            json_dic[Deal.COMMISSION_CLOSE_F] = closed_self.commission_close
        return json.dumps(json_dic)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        deal = Deal(datetime.fromisoformat(data[Deal.OPEN_DATE_F]), 
                    data[Deal.OPEN_PRICE_F], 
                    data[Deal.AMOUNT_F], 
                    data[Deal.ASSET_F],
                    data[Deal.USING_CAP_F],
                    data[Deal.COMMISSION_OPEN_F])
        
        deal.add_commision_holding(data[Deal.COMMISSION_HOLDING_F])
        
        if data[Deal.IS_CLOSED] == 1:
            deal.close_deal(
                datetime.fromisoformat(data[Deal.CLOSE_DATE_F]),
                data[Deal.CLOSE_PRICE_F],
                data[Deal.COMMISSION_CLOSE_F])
        return deal

class CloseDeal(Deal):
    @property
    def close_date(self) -> datetime:
        return super().close_date# type: ignore

    @property
    def close_price(self) -> float:
        return super().close_price# type: ignore
    
    @property
    def profit(self) -> float:
        return super().profit# type: ignore

    @property
    def interest(self) -> float:
        return super().interest# type: ignore