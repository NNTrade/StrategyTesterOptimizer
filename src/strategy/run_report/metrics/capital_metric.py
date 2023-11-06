from ...absStrategy import Dict, datetime, MarketConfig

class CapitalMetric:
    STR_YIELD_F = "strategy_yield"
    STR_MAX_YIELD_F = "strategy_max_yield"
    MAX_FALL_F = "max_fall"
    STR_YIELD_YEAR_F = "strategy_yield_per_year"

    def __init__(self, market_config: MarketConfig, capital_log: Dict[datetime, float]) -> None:
        if len(capital_log) == 0:
            raise AttributeError(
                "No infarmation about capitol, must be at least one record", name="strategy.abs_capital_log")

        start_cap = capital_log[min(capital_log.keys())]
        last_cap = capital_log[max(
            capital_log.keys())]
        self.__strategy_yield = last_cap/start_cap - 1
        self.__strategy_max_yield = max(capital_log.values())/start_cap - 1

        self.__calc_max_loss(capital_log, start_cap)
        self.__market_config: MarketConfig = market_config
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
    def strategy_yield(self) -> float:
        """Result yeield: (Income - Loss - Commission)/start_cap - 1

        Returns:
            float: Strategy Yield
        """
        return self.__strategy_yield
    

    @property
    def strategy_max_yield(self) -> float:
        """Maximum strategy yield gained due to strategy run

        Returns:
            float: Max Strategy Yield
        """
        return self.__strategy_max_yield

    @property
    def max_fall(self) -> float:
        """Max downfall = - (max - min) / max. -1 - loss all, 0 - no losses

        Returns:
            float: max downfall
        """
        return self.__max_fall

    @property
    def strategy_yield_per_year(self) -> float:
        """Result yeield per year

        Returns:
            float: Strategy Yield per year
        """
        return pow((self.strategy_yield + 1), 1/self.__market_config.period_in_years) - 1

    def to_dict(self) -> Dict:
        return {
           CapitalMetric.STR_YIELD_F: self.strategy_yield,
           CapitalMetric.STR_YIELD_YEAR_F: self.strategy_yield_per_year,
           CapitalMetric.STR_MAX_YIELD_F: self.strategy_max_yield,
           CapitalMetric.MAX_FALL_F: self.max_fall
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash(tuple(self.to_dict().values()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CapitalMetric):
            return False
        return self.to_dict() == other.to_dict()