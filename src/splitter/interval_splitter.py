from typing import List
from ..common.date_period import DatePeriod
import numpy as np
from datetime import timedelta

def split_period(period:DatePeriod, proportions:List[int])->List:
    total_proportion = np.sum(proportions)

    days_in_one = period.period_in_days / total_proportion
    ret_periods: List[DatePeriod] = []
    last_untill_date = period.from_date

    for proportion in proportions:
        proportion_days = days_in_one * proportion
        untill_date = last_untill_date + timedelta(days=proportion_days)

        if untill_date > period.untill_date:
            untill_date = period.untill_date

        ret_periods.append(DatePeriod(last_untill_date, untill_date))

        if untill_date == period.untill_date:
            break
        
        last_untill_date = untill_date

    assert len(ret_periods) == len(
        proportions), "Cann't make same amount of proportion as needed"

    return ret_periods