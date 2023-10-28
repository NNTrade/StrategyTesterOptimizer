from ...absStrategy import Dict, datetime


class CapitalMetric:
    def __init__(self, capital_log: Dict[datetime, float]) -> None:
        if len(capital_log) == 0:
            raise AttributeError(
                "No infarmation about capitol, must be at least one record", name="strategy.abs_capital_log")

        start_cap = capital_log[min(capital_log.keys())]
        self.__net_profit = capital_log[max(
            capital_log.keys())]/start_cap
        self.__net_profit_max = max(capital_log.values())/start_cap

        self.__calc_max_loss(capital_log, start_cap)
        pass

    def __calc_max_loss(self, capital_log: Dict[datetime, float], start_cap):
        last_max = start_cap
        max_fall = 0
        for v in capital_log.values():
            if v >= last_max:
                last_max = v
            else:
                max_fall = max((last_max - v)/last_max, max_fall)
        self.__max_fall = -max_fall

    @property
    def net_profit(self) -> float:
        """Net profit (Income - Loss - Commission)

        Returns:
            float: Net Profit
        """
        return self.__net_profit

    @property
    def net_profit_max(self) -> float:
        """Maximum net profit gained due to strategy run

        Returns:
            float: Max Net Profit
        """
        return self.__net_profit_max

    @property
    def max_fall(self) -> float:
        """Max downfall = - (max - min) / max. -1 - loss all, 0 - no losses

        Returns:
            float: max downfall
        """
        return self.__max_fall