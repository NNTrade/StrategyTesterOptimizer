from __future__ import annotations
from datetime import date,timedelta
from typing import Dict,List
import pandas as pd

class DatePeriod:
    """Represent date interval
    """
    FROM_F = "from"
    UNTILL_F = "untill"
    DATE_COL_NAME = "Date"

    def __init__(self, from_date:date, untill_date:date):
        if from_date >= untill_date:
            raise AttributeError("From date must be less then untill date")
        self.__from_date = from_date
        self.__untill_date = untill_date

    @property
    def from_date(self) -> date:
        """Stock ticker name
        """
        return self.__from_date

    @property
    def untill_date(self) -> date:
        """Timeframe of candle data
        """
        return self.__untill_date
    
    @property
    def period_in_days(self)->int:
        """retun delta between fram_date and untill_date in days

        Returns:
            float: days in config
        """
        return (self.untill_date - self.from_date).days
    
    @property
    def period_in_years(self)->float:
        """retun delta between fram_date and untill_date in years

        Returns:
            float: years in config
        """
        return self.period_in_days/365
    
    
    def filter_df(self, df:pd.DataFrame,date_col:str|None = None)-> pd.DataFrame:
        if date_col is None:
            from_date = pd.to_datetime(self.__from_date)
            until_date = pd.to_datetime(self.__untill_date)

            # Filter the DataFrame based on the date range
            return df[(df.index >= from_date) & (df.index < until_date)]
        else:
            return df[(df[date_col]>=self.__from_date.strftime("%Y-%m-%d")) & (df[date_col]<self.__untill_date.strftime("%Y-%m-%d"))]

    def split(self, chunks_count: int) -> List[DatePeriod]:
        ts = self.untill_date - self.from_date
        step_ts = timedelta(days=int(ts.days/chunks_count))
        cur_dt = self.from_date
        ret_cfg = []
        for i in range(chunks_count-1):
            new_untill = cur_dt + step_ts
            if new_untill > self.untill_date:
                new_untill = self.untill_date
            ret_cfg.append(DatePeriod(cur_dt, new_untill))
            cur_dt = new_untill
        ret_cfg.append(DatePeriod(cur_dt, self.untill_date))
        return ret_cfg
    
    def to_dict(self) -> Dict:
        return {
            DatePeriod.FROM_F: self.from_date,
            DatePeriod.UNTILL_F: self.untill_date,
        }

    def __str__(self):
        return f"{self.from_date} - {self.untill_date}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((self.from_date, self.untill_date))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DatePeriod):
            return False
        return self.to_dict() == other.to_dict()

    def __lt__(self, other):
        # Custom less-than comparison for sorting
        key_order = [
            self.FROM_F, self.UNTILL_F
        ]
        for key in key_order:
            if getattr(self, key) != getattr(other, key):
                return getattr(self, key) > getattr(other, key)
        return False