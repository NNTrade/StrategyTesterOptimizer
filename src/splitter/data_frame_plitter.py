import logging
from tkinter import NO
from typing import List

from pandas import DataFrame, Series


class DataFrameSplitter:
    @staticmethod
    def split_data(data: DataFrame|Series,propotions:List[int], shift:int|None = None, cut_tail:bool = True) -> List[List[DataFrame|Series]]:
        return DataFrameSplitter(propotions, shift, cut_tail).split(data)
    
    def __init__(self, propotions:List[int], shift:int|None = None, cut_tail:bool = True) -> None:
        """_summary_

        Args:
            proprotions (List[int]): proportions of dataframe split
            cut_tail (bool, optional): remove check that if current DataFrame doesn't cutted sharped. Defaults to True.
        """
        self.cut_tail = cut_tail
        self.__logger = logging.getLogger(type(DataFrameSplitter).__name__)
        self.__proportions: List[int] = propotions
        self.__shift = sum(propotions) if shift is None else shift

    @property
    def proportions(self) -> List[int]:
        return self.__proportions.copy()
    
    def split(self, data: DataFrame|Series) -> List[List[DataFrame|Series]]:
        """splitt date period to list of optimization and forward analization periods
        """
        ','.join([str(p) for p in self.__proportions])
        self.__logger.info(f"Splitting data on proportios: ({','.join([str(p) for p in self.__proportions])})")
        
        return_intervals = []
        cur_idx = 0       
        data_len = len(data)

        while cur_idx < data_len:
            start_sub_interval = cur_idx
            end_sub_interval = start_sub_interval
            sub_set = []
            for porportion in self.__proportions:
                end_sub_interval = start_sub_interval + porportion
                sub_set.append(data.iloc[start_sub_interval: end_sub_interval])
                start_sub_interval = end_sub_interval
            if end_sub_interval <= data_len:
                return_intervals.append(sub_set)
                if end_sub_interval == data_len:
                    break
            else:
                if not self.cut_tail:
                    raise AttributeError(
                        "Cannot split interval on round parts")
            cur_idx = cur_idx + self.__shift

        return return_intervals
