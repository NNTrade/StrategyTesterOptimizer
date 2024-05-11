from __future__ import annotations
import logging
from re import sub
from ..common.date_period import DatePeriod
from datetime import timedelta
from typing import List, Tuple


class DatePeriodSplitter:
    @staticmethod
    def from_days(proportions_in_days: List[int], cut_tail: bool = True) -> DatePeriodSplitter:
        return DatePeriodSplitter([timedelta(proportion_in_days) for proportion_in_days in proportions_in_days], cut_tail)

    @staticmethod
    def default_tf_d() -> DatePeriodSplitter:
        return DatePeriodSplitter.from_days([360, 60])

    @staticmethod
    def split_date_period(date_period: DatePeriod, sub_intervals: List[timedelta | int], cut_tail: bool = True) -> List[List[DatePeriod]]:
        """Split date period into sub intervals by given proportions config

        Args:
            date_period (DatePeriod): Date period for split
            sub_intervals (List[timedelta | int]): proportions for splitting, if pass int value it converts as timedelta of int days
            cut_tail (bool, optional): Cut tail of date period if date period doesn't cut fully. Defaults to True.

        Raises:
            AttributeError: sub_intervals has invalid type

        Returns:
            List[List[DatePeriod]]: list of sub intervals date periods
        """
        using_proportions = []
        for proportion in sub_intervals:
            if isinstance(proportion, int):
                using_proportions.append(timedelta(proportion))
            elif isinstance(proportion, timedelta):
                using_proportions.append(proportion)
            else:
                raise AttributeError(
                    "Wrong type of proportion %s", type(proportion))

        return DatePeriodSplitter(using_proportions, cut_tail).split(date_period)

    def __init__(self, proportions: List[timedelta], cut_tail: bool = True):
        """_summary_

        Args:
        proportions (List[timedelta]): proportions of dateperiod split
        cut_tail (bool, optional): remove check that if current time interval doesn't cutted sharped. Defaults to True.
        """
        self.cut_tail = cut_tail
        self.__logger = logging.getLogger(type(DatePeriodSplitter).__name__)
        self.__proportions: List[timedelta] = proportions

    @property
    def proportions(self) -> List[timedelta]:
        return self.__proportions.copy()

    def split(self, date_period: DatePeriod) -> List[List[DatePeriod]]:
        """splitt date period to list of optimization and forward analization periods
        """
        ','.join([str(p) for p in self.__proportions])
        self.__logger.info(f"Splitting {date_period} on proportios: ({
                           ','.join([str(p) for p in self.__proportions])})")
        return_intervals = []
        start_sub_interval = date_period.from_date
        end_sub_interval = start_sub_interval
        
        while end_sub_interval < date_period.untill_date:
            sub_set = []
            for porportion in self.__proportions:
                end_sub_interval = start_sub_interval + porportion
                sub_set.append(DatePeriod(start_sub_interval, end_sub_interval))
                start_sub_interval = end_sub_interval
            if end_sub_interval <= date_period.untill_date:
                return_intervals.append(sub_set)
            else:
                if not self.cut_tail:
                    raise AttributeError(
                        "Cannot split interval on round parts")

        return return_intervals
