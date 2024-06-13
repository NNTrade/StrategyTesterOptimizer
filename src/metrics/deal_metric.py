from datetime import timedelta
from math import sqrt
import pprint
from ..models.deal import Deal
from typing import Tuple, Union,List,Dict
import numpy as np

class DealMetric:
    DEAL_COUNT_F = "deal_count"
    SUCCESS_DEAL_COUNT_F = "success_deal_count"
    FAIL_DEAL_COUNT_F = "fail_deal_count"
    AVG_NET_PROFIT_BY_SUCCESS_F = "avg_net_profit_by_success"
    AVG_NET_PROFIT_BY_LOSS_F = "avg_net_profit_by_loss"
    AVG_NET_PROFIT_F = "avg_net_profit"
    AVG_INTEREST_TO_ACC_BY_SUCCESS_F = "avg_interest_to_account_by_success"
    AVG_INTEREST_TO_ACC_BY_LOSS_F = "avg_interest_to_account_by_loss"
    AVG_INTEREST_TO_ACC_F = "avg_interest_to_account"
    AVG_INTEREST_TO_POS_BY_SUCCESS_F = "avg_interest_to_position_by_success"
    AVG_INTEREST_TO_POS_BY_LOSS_F = "avg_interest_to_position_by_loss"
    AVG_INTEREST_TO_POS_F = "avg_interest_to_position"
    AVG_INTEREST_TO_ACC_PER_YEAR_BY_SUCCESS_F = "avg_interest_to_account_per_year_by_success"
    AVG_INTEREST_TO_ACC_PER_YEAR_BY_LOSS_F = "avg_interest_to_account_per_year_by_loss"
    AVG_INTEREST_TO_ACC_PER_YEAR_F = "avg_interest_to_account_per_year"
    AVG_INTEREST_TO_POS_PER_YEAR_BY_SUCCESS_F = "avg_interest_to_position_per_year_by_success"
    AVG_INTEREST_TO_POS_PER_YEAR_BY_LOSS_F = "avg_interest_to_position_per_year_by_loss"
    AVG_INTEREST_TO_POS_PER_YEAR_F = "avg_interest_to_position_per_year"
    AVG_DEAL_LENGHT_IN_DAYS_F = "avg_deal_len_in_days"
    PROM_F = "PROM"

    @staticmethod
    def get_avg_interest(deal_list:List[Deal])->Tuple[float,float,float,float]:
        """_summary_

        Args:
            deal_list (List[Deal]): list of deals

        Returns:
            Tuple[float,float,float,float]: avg_interest_to_pos, avg_interest_to_acc,avg_interest_to_pos_per_year,avg_interest_to_acc_per_year
        """
        avg_interest_to_pos = float(np.mean([d.interest_to_position for d in deal_list]))
        avg_interest_to_acc = float(np.mean([d.interest_to_account for d in deal_list]))
        avg_interest_to_pos_per_year = float(pow(np.prod([d.interest_to_position for d in deal_list]),365/np.sum([d.lenght_in_days.days for d in deal_list])))
        avg_interest_to_acc_per_year = float(pow(np.prod([d.interest_to_account for d in deal_list]),365/np.sum([d.lenght_in_days.days for d in deal_list])))
        return avg_interest_to_pos, avg_interest_to_acc,avg_interest_to_pos_per_year,avg_interest_to_acc_per_year
    
    def __init__(self, deal_list: List[Deal]) -> None:
        self.__deal_count = len(deal_list)

        success_deals = [d for d in deal_list if d.profit > 0]
        self.__success_deal_count = len(success_deals)
        
        fail_deals = [d for d in deal_list if d.profit < 0]
        self.__fail_deal_count = len(fail_deals)

        closed_deals_len = [d.lenght_in_days.days for d in deal_list if d.is_closed] # type: ignore
        self.__avg_deal_length_in_days = float(np.mean(closed_deals_len)) if len(closed_deals_len) else None

        if self.__deal_count > 0:
            self.__avg_profit_all = float(np.mean([d.profit for d in deal_list]))
            self.__avg_interest_to_pos, self.__avg_interest_to_acc, self.__avg_interest_to_pos_per_year, self.__avg_interest_to_acc_per_year  = DealMetric.get_avg_interest(deal_list)
        else:
            self.__avg_profit_all = None
            self.__avg_interest_to_pos = None
            self.__avg_interest_to_acc = None
            self.__avg_interest_to_pos_per_year = None 
            self.__avg_interest_to_acc_per_year = None

        if self.__success_deal_count > 0:
            self.__avg_profit_by_success = float(np.mean([d.profit for d in success_deals]))
            self.__avg_interest_to_pos_by_success, self.__avg_interest_to_acc_by_success, self.__avg_interest_to_pos_per_year_by_success, self.__avg_interest_to_acc_per_year_by_success  = DealMetric.get_avg_interest(success_deals)
        else:
            self.__avg_profit_by_success = 0
            self.__avg_interest_to_pos_by_success =0
            self.__avg_interest_to_acc_by_success = 0
            self.__avg_interest_to_pos_per_year_by_success = 0
            self.__avg_interest_to_acc_per_year_by_success = 0

        if self.__fail_deal_count > 0:
            self.__avg_profit_by_loss = float(np.mean([d.profit for d in fail_deals]))
            self.__avg_interest_to_pos_by_loss, self.__avg_interest_to_acc_by_loss, self.__avg_interest_to_pos_per_year_by_loss, self.__avg_interest_to_acc_per_year_by_loss  = DealMetric.get_avg_interest(fail_deals)
        else:
            self.__avg_profit_by_loss = 0
            self.__avg_interest_to_pos_by_loss = 0
            self.__avg_interest_to_acc_by_loss = 0
            self.__avg_interest_to_pos_per_year_by_loss = 0 
            self.__avg_interest_to_acc_per_year_by_loss = 0
        pass

    @property
    def PROM(self)->Union[float, None]:
        """The pessimistic return on margin

        Returns:
            Union[float, None]: The pessimistic return on margin. If no success or fail deals then None
        """
        M = self.avg_profit_by_success * self.success_deal + self.avg_profit_by_loss * self.fail_deal
        if M == 0:
            return None
        
        AGP = self.avg_profit_by_success * (self.success_deal - sqrt(self.success_deal))
        AGL = self.avg_profit_by_loss * (self.fail_deal + sqrt(self.fail_deal))

        return (AGP + AGL)/M

    @property
    def avg_profit_all(self)->Union[float, None]:
        """Average deal profit. If no deals then None

        Returns:
            Union[float,None]: average deal net income
        """
        return self.__avg_profit_all
    
    @property
    def avg_profit_by_success(self)->float:
        """Income per seccess deal\n
        Average gain cash per success deal. If no nuccess deals then 0

        Returns:
            Union[float,None]: average deal net income >= 0
        """
        return self.__avg_profit_by_success
    
    @property
    def avg_profit_by_loss(self)->float:
        """Loss by loss deal.\n
        Average loss cash per loss deal. If no fail deals then 0

        Returns:
            Union[float,None]: average deal net loss <=0
        """
        return self.__avg_profit_by_loss

    @property
    def avg_interest_to_account_all(self)->Union[float, None]:
        """Average deal interest relative to account capital. If no deals then None

        Returns:
            Union[float,None]: average deal net income
        """
        return self.__avg_interest_to_acc
    
    @property
    def avg_interest_to_position_all(self)->Union[float, None]:
        """Average deal interest relative to position open size (open price * amount). If no deals then None

        Returns:
            Union[float,None]: average deal net income
        """
        return self.__avg_interest_to_pos
    
    @property
    def avg_interest_to_account_per_year_all(self)->Union[float, None]:
        """Average deal interest per year relative to account capital. If no deals then None

        Returns:
            Union[float,None]: average deal net income
        """
        return self.__avg_interest_to_acc_per_year
    
    @property
    def avg_interest_to_position_per_year_all(self)->Union[float, None]:
        """Average deal interest per year relative to position open size (open price * amount) ^ (365/deal_lenght_in_days). If no deals then None

        Returns:
            Union[float,None]: average deal net income
        """
        return self.__avg_interest_to_pos_per_year
    
    @property
    def avg_interest_to_account_by_success(self)->float:
        """Average interest by success deal relative to account capital. If no nuccess deals then 0

        Returns:
            Union[float,None]: average deal net income >= 0
        """
        return self.__avg_interest_to_acc_by_success
    
    @property
    def avg_interest_to_position_by_success(self)->float:
        """Average interest by success deal relative to position open size (open price * amount)^(365/lenght_in_days). If no nuccess deals then 0

        Returns:
            Union[float,None]: average deal net income >= 0
        """
        return self.__avg_interest_to_pos_by_success
    
    @property
    def avg_interest_to_account_per_year_by_success(self)->float:
        """Average interest per year by success deal relative to account capital. If no nuccess deals then 0

        Returns:
            Union[float,None]: average deal net income >= 0
        """
        return self.__avg_interest_to_acc_per_year_by_success
    
    @property
    def avg_interest_to_position_per_year_by_success(self)->float:
        """Average interest per year by success deal relative to position open size (open price * amount). If no nuccess deals then 0

        Returns:
            Union[float,None]: average deal net income >= 0
        """
        return self.__avg_interest_to_pos_per_year_by_success
    
    @property
    def avg_interest_to_account_by_loss(self)->float:
        """Average interest by loss deal relative to account capital. If no fail deals then 0

        Returns:
            Union[float,None]: average deal net loss <=0
        """
        return self.__avg_interest_to_acc_by_loss
    
    @property
    def avg_interest_to_position_by_loss(self)->float:
        """Average interest by loss deal relative to position open size (open price * amount). If no fail deals then 0

        Returns:
            Union[float,None]: average deal net loss <=0
        """
        return self.__avg_interest_to_pos_by_loss
    
    @property
    def avg_interest_to_account_per_year_by_loss(self)->float:
        """Average interest per year by loss deal relative to account capital. If no fail deals then 0

        Returns:
            Union[float,None]: average deal net loss <=0
        """
        return self.__avg_interest_to_acc_per_year_by_loss
    
    @property
    def avg_interest_to_position_per_year_by_loss(self)->float:
        """Average interest per year by loss deal relative to position open size (open price * amount)^(365/lenght_in_days). If no fail deals then 0

        Returns:
            Union[float,None]: average deal net loss <=0
        """
        return self.__avg_interest_to_pos_per_year_by_loss

    @property
    def avg_deal_lenght_in_days(self)->float|None:
        return self.__avg_deal_length_in_days

    @property
    def deal_count(self) -> int:
        """Totap deal counts

        Returns:
            int: deal counts
        """
        return self.__deal_count

    @property
    def success_deal(self) -> int:
        """Success deal count (result > 0)

        Returns:
            int: success deal count
        """
        return self.__success_deal_count

    @property
    def fail_deal(self) -> int:
        """Fail deal count (result < 0)

        Returns:
            int: fail deal count
        """
        return self.__fail_deal_count

    def to_dict(self) -> Dict:
        return {
            DealMetric.DEAL_COUNT_F: self.deal_count,
            DealMetric.SUCCESS_DEAL_COUNT_F: self.success_deal,
            DealMetric.FAIL_DEAL_COUNT_F: self.fail_deal,
            DealMetric.AVG_DEAL_LENGHT_IN_DAYS_F: self.avg_deal_lenght_in_days,
            DealMetric.AVG_NET_PROFIT_F: self.avg_profit_all,
            DealMetric.AVG_NET_PROFIT_BY_SUCCESS_F: self.avg_profit_by_success,
            DealMetric.AVG_NET_PROFIT_BY_LOSS_F: self.avg_profit_by_loss,
            DealMetric.AVG_INTEREST_TO_POS_BY_SUCCESS_F:self.avg_interest_to_position_by_success,
            DealMetric.AVG_INTEREST_TO_POS_BY_LOSS_F:self.avg_interest_to_position_by_loss, 
            DealMetric.AVG_INTEREST_TO_POS_F:self.avg_interest_to_position_all,
            DealMetric.AVG_INTEREST_TO_ACC_BY_SUCCESS_F:self.avg_interest_to_account_by_success,
            DealMetric.AVG_INTEREST_TO_ACC_BY_LOSS_F:self.avg_interest_to_account_by_loss, 
            DealMetric.AVG_INTEREST_TO_ACC_F:self.avg_interest_to_account_all,
            DealMetric.AVG_INTEREST_TO_POS_PER_YEAR_BY_SUCCESS_F:self.avg_interest_to_position_per_year_by_success,
            DealMetric.AVG_INTEREST_TO_POS_PER_YEAR_BY_LOSS_F:self.avg_interest_to_position_per_year_by_loss, 
            DealMetric.AVG_INTEREST_TO_POS_PER_YEAR_F:self.avg_interest_to_position_per_year_all,
            DealMetric.AVG_INTEREST_TO_ACC_PER_YEAR_BY_SUCCESS_F:self.avg_interest_to_account_per_year_by_success,
            DealMetric.AVG_INTEREST_TO_ACC_PER_YEAR_BY_LOSS_F:self.avg_interest_to_account_per_year_by_loss, 
            DealMetric.AVG_INTEREST_TO_ACC_PER_YEAR_F:self.avg_interest_to_account_per_year_all,
            DealMetric.PROM_F: self.PROM
        }

    def __str__(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(tuple(self.to_dict().values()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DealMetric):
            return False
        return self.to_dict() == other.to_dict()
