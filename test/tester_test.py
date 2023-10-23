import unittest
import logging
from src.testing.tester import Tester
from src.Strategy import StrategyFactory
from src.strategy.run_config import RunConfigSet, date


class Tester_TestCase(unittest.TestCase):
  class FakeStrategi:
    def __init__(self, p1: int, p2: int) -> None:
      self.p1 = p1
      self.p2 = p2
      pass
    def
  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_give_strategy_and_run_test_THEN_get_correct_result(self):
    # Array
    rc = RunConfigSet.buildSameTradeInterval(
        ["s1", "s2"], date(2020, 1, 1), date(2021, 1, 1), parameters=["p1":[1, 2, 3], "p2":[4, 5, 6]])
    mockSF = StrategyFactory()

    tester = Tester(mockSF)

    # Act
    report = tester.run(rc)

    # Assert
