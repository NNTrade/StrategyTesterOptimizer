from ...absStrategy import Deal, List


class DealMetric:
    def __init__(self, deal_list: List[Deal]) -> None:
        self.__deal_count = len(deal_list)
        self.__success_deal_count = len(
            [d for d in deal_list if d.result > 0])
        self.__fail_deal_count = len(
            [d for d in deal_list if d.result < 0])
        pass

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
