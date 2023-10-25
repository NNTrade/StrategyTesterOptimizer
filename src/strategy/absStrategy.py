from __future__ import annotations
from .deal import Deal
from abc import ABC
from datetime import date, datetime
from typing import Dict, List


class absStrategy(ABC):
  # TODO [FI-85]: Описать abstract Strategy
  """Abstraction of strategy
  """

  @property
  def abs_capital_log(self) -> Dict[datetime, float]:
    """abstract capital log. Initial capital start from 1 other capital based on this value

    Returns:
        Dict[datetime, float]: Log of changing base capital
    """
    ...

  @property
  def deal_list(self) -> List[Deal]:
    ...

  def run(self, stock_list: List[str], from_date: date, till_date: date) -> absStrategy:
    """run strategy for maket list on period from_date till_date

    Args:
        stock_list (List[str]): _description_
        from_date (date): _description_
        till_date (date): _description_
    """
    ...

  class Factory(ABC):
    # TODO: [FI-86] Описать abstract Strategy.Factory
    """Factory for builing new strategy instance in each test
    """

    def build(self, parameters: Dict) -> absStrategy:
      ...
