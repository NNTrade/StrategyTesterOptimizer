import unittest
import logging
import src.strategy.run_config as cfg
from src.strategy.run_report import  absTradingSimulationFactory
from src.simulation.simulation_report import SimulationReport
from src.testing_report import TestingReport 
from datetime import datetime
from src.simulation.deal import Deal

class TestingReport_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
      
  def test_WHEN_run_THEN_ok(self):
    # Array
    si = cfg.StrategyId("test", "1.0")

    # test set 1
    sc_set1 = cfg.StrategyConfig({"P1": 1,"P2": 2})
    rc1 = cfg.RunConfig(
        cfg.MarketConfig([cfg.StockConfig("S1", cfg.TimeFrame.D)],cfg.TimeFrame.D, cfg.date(2020, 1, 1), cfg.date(2021, 1, 1)),
        sc_set1)
    cap1 = {
      datetime(2020,1,1):100.0,
      datetime(2020,1,2):102
    }
    deal_list1 = [
      Deal(datetime(2020,1,1),100,datetime(2020,1,10),120,1,100),
      Deal(datetime(2020,1,10),120,None,90,-1,120)
    ]
    rr = SimulationReport(si, rc1, cap1,deal_list1)
    # Act
    asserted_r = TestingReport([rr])

    # Assert
    print(asserted_r.as_df)