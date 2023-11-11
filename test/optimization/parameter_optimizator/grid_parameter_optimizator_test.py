import unittest
import logging
from src.optimization.parameter_optimizator import GridParameterOptimizator, StrategyConfigSet
from src.strategy.run_config.strategy_config import StrategyConfig

class GridParameterOptimizator_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_call_THEN_work_correct(self):
    # Array
    scs = StrategyConfigSet({"A":[1,2,3], "B":[1,2,3]}, lambda cfg: cfg["A"] != cfg["B"])
    gpo = GridParameterOptimizator(scs, lambda rr1,rr2: hash(rr2) - hash(rr1))
    
    expected_cfgs = [
      StrategyConfig({"A":1,"B":2}),
      StrategyConfig({"A":1,"B":3}),
      StrategyConfig({"A":2,"B":1}),
      StrategyConfig({"A":2,"B":3}),
      StrategyConfig({"A":3,"B":1}),
      StrategyConfig({"A":3,"B":2})
    ]

    def step(rr_val):
      # Array 3    
      l_used_rr = rr_val
      # Act 3
      l_sc = gpo.next(l_used_rr) # type: ignore
      # Assert 3
      self.assertIsNotNone(l_sc)
      self.assertIn(l_sc, expected_cfgs)
      expected_cfgs.remove(l_sc) # type: ignore
    
    # Act 1
    sc1 = gpo.first()
    
    # Assert 1
    self.assertIn(sc1, expected_cfgs)
    expected_cfgs.remove(sc1)

    step(1)
    step(2)
    step(30)
    step(4)
    step(5)

    sc_last = gpo.next(6)# type: ignore
    self.assertIsNone(sc_last)

    asserted_best = gpo.best()
    self.assertEqual(30, asserted_best)