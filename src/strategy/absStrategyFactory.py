from src.strategy.absStrategy import absStrategy


from abc import ABC
from typing import Dict


class absStrategyFactory(ABC):
  # TODO: [FI-86] Описать abstract Strategy.Factory
  """Factory for builing new strategy instance in each test
  """

  def build(self, parameters: Dict) -> absStrategy:
    ...
