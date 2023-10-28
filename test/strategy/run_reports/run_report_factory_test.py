from __future__ import annotations
from typing import Dict, List, Union
import unittest
import logging
from src.strategy.absStrategy import absStrategy
from src.strategy.run_report import RunReport, RunConfig, Deal, RunReportFactory, Storage
from src.strategy.run_config import MarketConfig
from datetime import date, datetime, timedelta


class Factory_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    class FakeStr(absStrategy):
        def __init__(self) -> None:
            self._capital_log = {}
            self._deal = []
            super().__init__()

        def run(self, market_cfg: MarketConfig):
            cur_d = market_cfg.from_date
            cap = 1
            self._deal.append(
                Deal(cur_d, cap, cur_d+timedelta(days=2), cap+1, cap))
            while cur_d < market_cfg.untill_date:
                self._capital_log[cur_d] = cap
                cap = cap + 1
                cur_d = cur_d + timedelta(days=1)
            return self

        @property
        def abs_capital_log(self) -> Dict[datetime, float]:
            return self._capital_log.copy()

        @property
        def deal_list(self) -> List[Deal]:
            return self._deal.copy()

    class FakeFactory(absStrategy.Factory):
        def __init__(self) -> None:
            super().__init__()

        def build(self, parameters: Dict) -> absStrategy:
            return Factory_TestCase.FakeStr()

    def test_WHEN_request_report_THEN_get_correct_report(self):
        # Array
        ff = Factory_TestCase.FakeFactory()
        rrf = RunReportFactory(ff)
        rc = RunConfig(MarketConfig(
            ["S1", "S2"], date(2020, 1, 1), date(2020, 1, 5)))

        expected_cap_log = {
            date(2020, 1, 1): 1,
            date(2020, 1, 2): 2,
            date(2020, 1, 3): 3,
            date(2020, 1, 4): 4
        }

        expected_deals = [
            Deal(date(2020, 1, 1), 1, date(2020, 1, 1) +
                 timedelta(days=2), 2, 1, 0, 0, 0)
        ]
        # Act
        asserted_rr = rrf.get(rc)

        # Assert
        self.assertEqual(4, len(asserted_rr.abs_capital_log))
        for i in [1, 2, 3, 4]:
            self.assertEqual(i, asserted_rr.abs_capital_log[date(2020, 1, i)])

        self.assertEqual(1, len(asserted_rr.deal_list))
        self.assertEqual(expected_deals[0], asserted_rr.deal_list[0])

    def test_WHEN_report_storage_has_report_THEN_return_it(self):
        # Array
        rc = RunConfig(MarketConfig(
            ["S1", "S2"], date(2020, 1, 1), date(2020, 1, 5)))
        expected_run_report = RunReport(
            Factory_TestCase.FakeStr().run(rc.market_cfg))

        class ReportStorage(Storage):
            def try_get(self, run_config: RunConfig) -> RunReport | None:
                if run_config == rc:
                    return expected_run_report
        rs = ReportStorage()
        ff = Factory_TestCase.FakeFactory()
        rrf = RunReportFactory(ff, rs)

        # Act
        asserted_rr = rrf.get(rc)

        # Assert
        self.assertTrue(asserted_rr == expected_run_report)
