from types import MappingProxyType
from .. import Strategy, Dict, datetime, Deal, List


class Report:
    # TODO: [FI-83] Описать RunReport
    """Report of strategy run
    """
    @property
    def abs_capital_log(self) -> Dict[datetime, float]:
        """Log of changing capital, init capital set to 1

        Returns:
            Dict[datetime, float]: _description_
        """
        return self.__capital_log

    @property
    def deal_list(self) -> List[Deal]:
        """List of deals

        Returns:
            List[Deal]: deal info
        """
        return self.__deal_list

    def __init__(self, strategy: Strategy) -> None:
        self.__capital_log = MappingProxyType(strategy.abs_capital_log.copy())
        self.__deal_list = tuple(strategy.deal_list.copy())
        pass
