from .absStrategy import absStrategy
from .run_config import StrategyConfig
from abc import ABC


class absStrategyFactory(ABC):
  """Factory for builing new strategy instance in each test
  """

  def build(self, parameters: StrategyConfig) -> absStrategy:
    ...
