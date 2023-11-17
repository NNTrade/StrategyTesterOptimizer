from __future__ import annotations
from typing import Dict, List, Union
import unittest
import logging
from src.strategy.run_report import RunReport, RunConfig, Deal, absRunReportFactory, absRunReportStorage
from src.strategy.run_config import MarketConfig, StrategyId, TimeFrame, StockConfig
from datetime import date, datetime, timedelta


class Factory_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


    class FakeFactory(absRunReportFactory):
        def __init__(self,report_storage: Union[absRunReportStorage,None] = None) -> None:
            super().__init__(report_storage)  

        def strategy_id(self)->StrategyId:
            return StrategyId("test", "0.0.1")

        def _run(self, run_config: RunConfig)->absRunReportFactory.RunResult:
            cur_d = datetime(run_config.market_cfg.from_date.year, run_config.market_cfg.from_date.month,run_config.market_cfg.from_date.day)
            cap = 1
            _capital_log = {}
            _deal = []
            _deal.append(Deal(cur_d, cap, cur_d+timedelta(days=2), cap+1, cap,cap))
            while cur_d.date() < run_config.market_cfg.untill_date:
                _capital_log[cur_d] = cap
                cap = cap + 1
                cur_d = cur_d + timedelta(days=1)
            return absRunReportFactory.RunResult(_capital_log, _deal)

    def test_WHEN_request_report_THEN_get_correct_report(self):
        # Array
        rrf = Factory_TestCase.FakeFactory()
        s1 = StockConfig("S1", TimeFrame.D)
        s2 = StockConfig("S2", TimeFrame.D)
        rc = RunConfig(MarketConfig(
            [s1, s2], TimeFrame.D, date(2020, 1, 1), date(2020, 1, 5)))

        expected_cap_log = {
            date(2020, 1, 1): 1,
            date(2020, 1, 2): 2,
            date(2020, 1, 3): 3,
            date(2020, 1, 4): 4
        }

        expected_deals = [
            Deal(datetime(2020, 1, 1), 1, datetime(2020, 1, 1) +
                 timedelta(days=2), 2, 1,1, 0, 0, 0)
        ]
        # Act
        asserted_rr = rrf.get(rc)

        # Assert
        self.assertEqual(4, len(asserted_rr.abs_capital_log))
        for i in [1, 2, 3, 4]:
            self.assertEqual(i, asserted_rr.abs_capital_log[datetime(2020, 1, i)])

        self.assertEqual(1, len(asserted_rr.deal_list))
        self.assertEqual(expected_deals[0], asserted_rr.deal_list[0])

    def test_WHEN_report_storage_has_report_THEN_return_it(self):
        # Array
        si = StrategyId("test", "0.0.1")
        s1 = StockConfig("S1", TimeFrame.D)
        s2 = StockConfig("S2", TimeFrame.D)
        rc = RunConfig(MarketConfig(
            [s1, s2], TimeFrame.m1, date(2020, 1, 1), date(2020, 1, 5)))
        expected_run_report = RunReport(si, rc,{datetime(2020,1,2):12},[])

        class ReportStorage(absRunReportStorage):
            def _try_get(self, run_config: RunConfig) -> Union[RunReport, None]:
                if run_config == rc:
                    return expected_run_report

            def _try_add(self, run_config: RunConfig, run_report: RunReport) -> bool:
                raise Exception("Unexpected")
        rs = ReportStorage()
        rrf = Factory_TestCase.FakeFactory(rs)

        # Act
        asserted_rr = rrf.get(rc)

        # Assert
        self.assertTrue(asserted_rr == expected_run_report)
