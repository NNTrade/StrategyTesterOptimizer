import unittest
import logging
from src.optimization.config import StrategyConfigSet,Union
from src.optimization.strategy.realization.grid_strategy import GridStrategy
from src.simulation.config import StrategyConfig,Dict

class GridParameterOptimizator_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  @staticmethod
  def buildCfg(dic: Dict[str,Union[int,float,str]])->Union[StrategyConfig,None]:
    if dic["A"] != dic["B"]:
      return StrategyConfig(dic)
    else:
      return None

  def test_WHEN_call_THEN_work_correct(self):
    # Array
    scs = StrategyConfigSet(GridParameterOptimizator_TestCase.buildCfg,{"A":[1,2,3], "B":[1,2,3]})
    gpo = GridStrategy(scs, lambda rr1,rr2: hash(rr2) - hash(rr1))
    
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