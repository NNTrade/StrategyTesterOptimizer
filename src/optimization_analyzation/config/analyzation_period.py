from ...common import DatePeriod
from typing import Dict

class AnalyzationPeriod:
    OPT_P_F = "optimization"
    FWD_P_F = "forward"

    def __init__(self, optimization_period:DatePeriod,forward_period: DatePeriod):
        if optimization_period.untill_date != forward_period.from_date:
            raise AttributeError("Optimization and forward period must be connected")
        self.__opt_p = optimization_period
        self.__fwd_p = forward_period

    @property
    def optimization_period(self) -> DatePeriod:
        """Stock ticker name
        """
        return self.__opt_p

    @property
    def forward_period(self) -> DatePeriod:
        """Timeframe of candle data
        """
        return self.__fwd_p
    
    @property
    def period_in_days(self)->int:
        """retun delta between fram_date and untill_date in days

        Returns:
            float: days in config
        """
        return (self.__fwd_p.untill_date - self.optimization_period.from_date).days
    
    @property
    def period_in_years(self)->float:
        """retun delta between fram_date and untill_date in years

        Returns:
            float: years in config
        """
        return self.period_in_days/36
    
    def to_dict(self) -> Dict:
        return {
            AnalyzationPeriod.OPT_P_F: self.optimization_period,
            AnalyzationPeriod.FWD_P_F: self.forward_period,
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((self.optimization_period, self.forward_period))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DatePeriod):
            return False
        return self.to_dict() == other.to_dict()