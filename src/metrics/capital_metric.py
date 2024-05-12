from datetime import datetime
import pprint
from ..models.deal import Deal
from ..common.date_period import DatePeriod,Dict,List
import numpy as np

class CapitalMetric:
    STR_YIELD_F = "yield"
    STR_MAX_YIELD_F = "max_yield"
    MAX_FALL_F = "max_fall"
    STR_YIELD_YEAR_F = "yield/year"
    CAPITAL_LOADING_LOG = "capital_load_log"
    AVG_CAPITAL_LOADING_LOG = "avg_capital_load_log"
    
    @staticmethod
    def calc_yield_total(final_cap, start_cap)->float:
        return final_cap/start_cap - 1
    
    @staticmethod
    def calc_yield_per_year(final_cap, start_cap, years):
        return pow((CapitalMetric.calc_yield_total(final_cap,start_cap) + 1), 1/years) - 1
    
    @staticmethod
    def calc_capital_loading_log(capital_log: Dict[datetime, float], deal_log:List[Deal])-> Dict[datetime, float]:
        opened_deal_in_date = {od: [d for d in deal_log if d.open_date==od] for od in capital_log.keys()}
        cur_open_deal:List[Deal] = []
        loading_cap_dict = {}
        for dt, cap in capital_log.items():
            deal_opened_in_this_day = opened_deal_in_date[dt]
            use_cap = 0
            for i in range(len(cur_open_deal)):
                deal = cur_open_deal.pop(0)
                try:
                    use_cap += deal.amount * deal.price_log[dt]
                except KeyError as ex:
                    raise KeyError(f"Cann't find price on date {dt} in deal {deal.id} opened {deal.open_date}")
                if deal.close_date != dt:
                    cur_open_deal.append(deal)

            for deal in deal_opened_in_this_day:
                try:
                    use_cap += deal.amount * deal.price_log[dt]
                except KeyError as ex:
                    raise KeyError(f"Cann't find price on date {dt} in deal {deal.id} opened {deal.open_date}")
                cur_open_deal.append(deal)
            loading_cap_dict[dt] = use_cap/cap
        return loading_cap_dict
    
    def __init__(self, date_config: DatePeriod, capital_log: Dict[datetime, float], deal_log:List[Deal]) -> None:
        if len(capital_log) == 0:
            raise AttributeError(
                "No infarmation about capitol, must be at least one record", name="strategy.abs_capital_log")

        self.__start_cap = capital_log[min(capital_log.keys())]
        self.__final_cap = capital_log[max(
            capital_log.keys())]
        self.__date_config: DatePeriod = date_config

        self.__strategy_yield = CapitalMetric.calc_yield_total(self.__final_cap,self.__start_cap)
        self.__strategy_yield_per_year = CapitalMetric.calc_yield_per_year(
                    self.__final_cap,
                    self.__start_cap, 
                    self.__date_config.period_in_years)

        self.__strategy_max_yield = max(capital_log.values())/self.__start_cap - 1

        self.__calc_max_loss(capital_log, self.__start_cap)
        self.__loading_log:Dict[datetime,float] = CapitalMetric.calc_capital_loading_log(capital_log,deal_log)
        pass

    def __calc_max_loss(self, capital_log: Dict[datetime, float], start_cap):
        last_max = start_cap
        max_fall = 0
        for v in capital_log.values():
            if v >= last_max:
                last_max = v
            else:
                max_fall = max((last_max - v)/last_max, max_fall)
        self.__max_fall = -max_fall
    
    @property
    def start_cap(self)->float:
        return self.__start_cap
    
    @property
    def final_cap(self)->float:
        return self.__final_cap
    
    @property
    def loading_log(self)->Dict[datetime,float]:
        return self.__loading_log.copy()
    
    @property
    def avg_loading_log(self)->float:
        return np.mean(list(self.__loading_log.values())) # type: ignore
    
    @property
    def strategy_yield(self) -> float:
        """Result yield: (Income - Loss - Commission)/start_cap - 1

        Returns:
            float: Strategy Yield
        """
        return self.__strategy_yield    

    @property
    def strategy_max_yield(self) -> float:
        """Maximum strategy yield gained due to strategy run

        Returns:
            float: Max Strategy Yield
        """
        return self.__strategy_max_yield

    @property
    def max_fall(self) -> float:
        """Max downfall = - (max - min) / max. -1 - loss all, 0 - no losses

        Returns:
            float: max downfall
        """
        return self.__max_fall

    @property
    def strategy_yield_per_year(self) -> float:
        """Result yield per year

        Returns:
            float: Strategy Yield per year
        """
        return self.__strategy_yield_per_year    

    def to_dict(self) -> Dict:
        return {
           CapitalMetric.STR_YIELD_F: self.strategy_yield,
           CapitalMetric.STR_YIELD_YEAR_F: self.strategy_yield_per_year,
           CapitalMetric.STR_MAX_YIELD_F: self.strategy_max_yield,
           CapitalMetric.MAX_FALL_F: self.max_fall,
           CapitalMetric.CAPITAL_LOADING_LOG: self.loading_log
        }

    def __str__(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(tuple(self.to_dict().values()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CapitalMetric):
            return False
        return self.to_dict() == other.to_dict()