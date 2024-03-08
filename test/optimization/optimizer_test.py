from __future__ import annotations
import datetime
import unittest
import logging
from src.optimization.optimizer import  absTradingSimulator,OptimizationConfig
from src.optimization.strategy.realization.grid_strategy import GridStrategyFactory
from src.optimization.config import StrategyConfigSet, StrategyConfig, Union,Dict
from src.simulation.config import CandleConfig,TimeFrame
from src.simulation import SimulationConfig, SimulationLog,StrategyId
from src.simulation.models import Deal,datetime
from src.simulation.cache.abs_simulation_log_storage import absSimulationLogStorage
from src.common import DatePeriod, CandleDataSetConfig,date
class Optimizer_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  @staticmethod
  def buildCfg(dic: Dict[str,Union[int,float,str]])->Union[StrategyConfig,None]:
    if dic["A"] != dic["B"]:
      return StrategyConfig(dic)
    else:
      return None
      
  class FakeSimulator(absTradingSimulator):
    def __init__(self, report_storage: absSimulationLogStorage | None = None) -> None:
      super().__init__(report_storage)
    def strategy_id(self)->StrategyId:
      return StrategyId("123", "zzz")
    def _run(self, run_config: SimulationConfig)->SimulationLog:
      if run_config.strategy_cfg["A"]==3 and run_config.strategy_cfg["B"] == 1:
        return SimulationLog({datetime(2020,1,1):1,datetime(2020,2,1):100},[Deal(datetime(2020,1,1),1,100,"abc",0.1).close_deal(datetime(2020,1,10),10)])
      return SimulationLog({datetime(2020,1,1):1,datetime(2020,2,1):10},[Deal(datetime(2020,1,1),1,10,"abc",0.1).close_deal(datetime(2020,1,10),2)])

  def test_WHEN_request_optimization_THEN_correct_optimization(self):
    # Array
    fs = Optimizer_TestCase.FakeSimulator()
    osf = GridStrategyFactory()

    opt = Optimizer(fs,osf)

    candle_ds_cfg = CandleDataSetConfig.BuildFrom(CandleConfig("A", TimeFrame.D),TimeFrame.D)
    dp = DatePeriod(date(2020,1,1), date(2020,2,2))
    scs = StrategyConfigSet({"A": [1,2,3], "B":[1,2,3]},Optimizer_TestCase.buildCfg)
    
    ocs = OptimizationConfig(candle_ds_cfg, dp,scs)

    # Act
    sr = opt.optimize(ocs)
    
    # Assert
    self.assertEqual(3,sr.simulation_config.strategy_cfg["A"])
    self.assertEqual(1,sr.simulation_config.strategy_cfg["B"])
    self.assertEqual(10,sr.deal_list[0].close_price)