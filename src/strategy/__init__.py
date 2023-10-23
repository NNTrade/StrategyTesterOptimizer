from __future__ import annotations
from typing import Dict
from abc import ABC


class Strategy(ABC):
  # TODO [FI-85]: Описать abstract Strategy
  """Abstraction of strategy
  """

  def run(self):
    ...

  class Factory(ABC):
    # TODO: [FI-86] Описать abstract Strategy.Factory
    """Factory for builing new strategy instance in each test
    """

    def build(self, parameters: Dict) -> Strategy:
      ...
