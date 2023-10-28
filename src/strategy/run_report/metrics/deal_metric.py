from ...absStrategy import Deal, List, Dict


class DealMetric:
    DEAL_COUNT_F = "deal_count"
    SUCCESS_DEAL_COUNT_F = "success_deal_count"
    FAIL_DEAL_COUNT_F = "fail_deal_count"

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

    def to_dict(self) -> Dict:
        return {
            DealMetric.DEAL_COUNT_F: self.deal_count,
            DealMetric.SUCCESS_DEAL_COUNT_F: self.success_deal,
            DealMetric.FAIL_DEAL_COUNT_F: self.fail_deal
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(tuple(self.to_dict().values()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DealMetric):
            return False
        return self.to_dict() == other.to_dict()
