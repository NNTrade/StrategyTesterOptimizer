from __future__ import annotations
from types import MappingProxyType
from typing import List, Dict
from datetime import date
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class RunConfig:
    """configuration of single strategy run
    """

    def __init__(self, stock_list: List[str], from_date: date, untill_date: date, parameters: Dict = {}):
        # Convert to a tuple to make it immutable
        self._stock_list = tuple(stock_list)
        self._from_date = from_date
        self._till_date = untill_date
        self._parameters = MappingProxyType(parameters)

    @property
    def stock_list(self) -> List[str]:
        return self._stock_list

    @property
    def from_date(self) -> date:
        return self._from_date

    @property
    def untill_date(self) -> date:
        return self._till_date

    @property
    def parameters(self) -> Dict:
        return self._parameters
