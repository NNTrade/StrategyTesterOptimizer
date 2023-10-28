from __future__ import annotations
from .deal import Deal
from abc import ABC
from datetime import datetime
from typing import Dict, List
from .run_config import MarketConfig


class absStrategy(ABC):
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

    def run(self, market_cfg: MarketConfig) -> absStrategy:
        """run strategy for maket list on period from_date untill_date

        Args:
            stock_list (List[str]): _description_
            from_date (date): _description_
            untill_date (date): _description_
        """
        ...
