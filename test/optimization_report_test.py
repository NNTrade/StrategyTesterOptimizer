import datetime
from pdb import run
import unittest
import logging
from src.optimization_report import OptimizationReport,RunConfigSet
from src.optimization.parameter_optimizator import GridParameterOptimizator
from src.optimization.market_config_splitter import DefaultMarketConfigSplitter
import src.strategy.run_config as rcl
import src.strategy.run_config.is_valid_checker
from src.strategy.run_config.strategy_config import StrategyConfig
from src.strategy.run_report import RunReport,absRunReportFactory
from src.strategy.run_config.market_config import MarketConfig
class OptimizationReport_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  class TestIsValidChecker(src.strategy.run_config.is_valid_checker.IsValidChecker[rcl.StrategyConfig]):
    def is_valid(self, validation_object: StrategyConfig) -> bool:
      return validation_object["P1"] != validation_object["P2"]
  class FakeRunReportFactory(absRunReportFactory):
      def strategy_id(self)->rcl.StrategyId:
        return rcl.StrategyId("test", "0.0.1")
      
      def _run(self, run_config: rcl.RunConfig)->absRunReportFactory.RunResult:
        
        cap ={
          datetime.datetime(run_config.market_cfg.from_date.year,run_config.market_cfg.from_date.month,run_config.market_cfg.from_date.day):1,
          datetime.datetime(run_config.market_cfg.from_date.year,run_config.market_cfg.from_date.month,run_config.market_cfg.from_date.day)+datetime.timedelta(days=10):run_config.strategy_cfg["P1"]*run_config.strategy_cfg["P2"]
        }
        return absRunReportFactory.RunResult(cap,[])
      
  def test_WHEN_run_THEN_ok(self):
    # Array
    rrf = OptimizationReport_TestCase.FakeRunReportFactory()
    pof = GridParameterOptimizator.Factory()
    mcs = DefaultMarketConfigSplitter.default_tf_d()
    orf = OptimizationReport.Factory(rrf, pof, mcs) # type: ignore
    ivc = OptimizationReport_TestCase.TestIsValidChecker()
    
    sc_set = rcl.StrategyConfigSet({"P1": [1,2],"P2": [1,2,3]}, ivc)
    rc = RunConfigSet(rcl.MarketConfigSet.Builder().add_stocks_set(
        [["S1"], ["S2"]], rcl.TimeFrame.D, rcl.date(2020, 1, 1), rcl.date(2021, 1, 1)).build(),
        sc_set)

    # Act
    opt_rep = orf.get(rc,False)


    # Assert
    self.assertEqual(6, opt_rep.forward_reports[0].metrics.capital.final_cap)