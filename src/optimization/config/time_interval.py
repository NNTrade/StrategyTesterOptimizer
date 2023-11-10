from __future__ import annotations
from ...strategy.run_config import MarketConfig, date,Dict

class TimeInterval:
  FROM_DT_F = MarketConfig.FROM_DATE_F
  UNTILL_DT_F = MarketConfig.UNTILL_DATE_F
  @staticmethod
  def extract_from(market_config:MarketConfig)->TimeInterval:
    return TimeInterval(market_config.from_date, market_config.untill_date)

  def __init__(self, from_date: date, untill_date: date) -> None:
    self.__from_date = from_date
    self.__untill_date = untill_date
    pass

  @property
  def from_date(self)->date:
    return self.__from_date
  
  @property
  def untill_date(self)->date:
    return self.__untill_date
  
  def to_dict(self) -> Dict:
    return {
        TimeInterval.FROM_DT_F: self.from_date,
        TimeInterval.UNTILL_DT_F: self.untill_date
    }

  def __str__(self):
      return f"{self.to_dict()}"

  def __repr__(self):
      return self.__str__()

  def __hash__(self):
      # Create a hash based on a tuple of hashable attributes
      return hash((self.from_date, self.untill_date))

  def __eq__(self, other: object) -> bool:
      if not isinstance(other, MarketConfig):
          return False
      return self.to_dict() == other.to_dict()
