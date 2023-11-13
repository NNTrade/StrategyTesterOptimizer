from __future__ import annotations
import unittest
import logging
from datetime import datetime
from src.strategy.run_report import RunReport, absStrategy, Dict, List, Deal
import src.strategy.run_config as cfg


class Report_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    class FakeStr(absStrategy):
        def __init__(self) -> None:
            self.deals = []
            self.cap = {}
            super().__init__()

        def set_deals(self, deals) -> Report_TestCase.FakeStr:
            self.deals = deals
            return self

        def set_cap(self, cap) -> Report_TestCase.FakeStr:
            self.cap = cap
            return self

        @property
        def abs_capital_log(self) -> Dict[datetime, float]:
            return self.cap

        @property
        def deal_list(self) -> List[Deal]:
            return self.deals

    def test_WHEN_empty_cap_THEN_exception(self):
        # Array
        used_str = Report_TestCase.FakeStr()
        si = cfg.StrategyId("test", "0.0.1")
        s1 = cfg.StockConfig("A", cfg.TimeFrame.D)
        s2 = cfg.StockConfig("B", cfg.TimeFrame.D)
        rc = cfg.RunConfig(si, cfg.MarketConfig([s1, s2], cfg.TimeFrame.D, cfg.date(2020, 1, 1),
                                                cfg.date(2021, 1, 1)), cfg.StrategyConfig({"p1": 1, "p2": 2}))
        # Act

        # Assert
        with self.assertRaises(AttributeError) as context:
            RunReport.build_from_strategy(rc, used_str)

    def test_WHEN_give_cap_in_wrong_order_THEN_correct_return_order(self):
        # Array
        si = cfg.StrategyId("test", "0.0.1")
        s1 = cfg.StockConfig("A", cfg.TimeFrame.D)
        s2 = cfg.StockConfig("B", cfg.TimeFrame.D)
        rc = cfg.RunConfig(si, cfg.MarketConfig([s1, s2], cfg.TimeFrame.D, cfg.date(2020, 1, 1),
                                                cfg.date(2021, 1, 1)), cfg.StrategyConfig({"p1": 1, "p2": 2}))
        expected_cap = {
            datetime(2023, 9, 1): 10.5,
            datetime(2023, 9, 3): 12.2,
            datetime(2023, 9, 2): 15.7,
        }
        used_str = Report_TestCase.FakeStr().set_cap(expected_cap)
        asserted_rep = RunReport.build_from_strategy(rc, used_str)

        # Act
        asserted_cap_log = asserted_rep.abs_capital_log

        # Assert
        self.assertEqual(3, len(asserted_cap_log))
        asserted_cap_log_as_list = [(k, v)
                                    for k, v in asserted_cap_log.items()]

        self.assertEqual(datetime(2023, 9, 1), asserted_cap_log_as_list[0][0])
        self.assertEqual(10.5, asserted_cap_log_as_list[0][1])

        self.assertEqual(datetime(2023, 9, 2), asserted_cap_log_as_list[1][0])
        self.assertEqual(15.7, asserted_cap_log_as_list[1][1])

        self.assertEqual(datetime(2023, 9, 3), asserted_cap_log_as_list[2][0])
        self.assertEqual(12.2, asserted_cap_log_as_list[2][1])

    def test_WHEN_equals_or_hash_THEN_correct_return(self):
        # Array
        si = cfg.StrategyId("test", "0.0.1")
        s1 = cfg.StockConfig("A", cfg.TimeFrame.D)
        s2 = cfg.StockConfig("B", cfg.TimeFrame.D)
        rc = cfg.RunConfig(si, cfg.MarketConfig([s1, s2], cfg.TimeFrame.D, cfg.date(2020, 1, 1),
                                                cfg.date(2021, 1, 1)), cfg.StrategyConfig({"p1": 1, "p2": 2}))

        base_rr = RunReport(rc,
                            {datetime(2023, 9, 1): 10.5,
                             datetime(2023, 9, 3): 12.2,
                             datetime(2023, 9, 2): 15.7,
                             },
                            [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1)])

        equal_rr_arr = [
            RunReport(rc,
                      {datetime(2023, 9, 1): 10.5,
                       datetime(2023, 9, 3): 12.2,
                       datetime(2023, 9, 2): 15.7,
                       },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1)]),
            RunReport(rc,
                      {datetime(2023, 9, 3): 12.2,
                       datetime(2023, 9, 1): 10.5,
                       datetime(2023, 9, 2): 15.7,
                       },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1)]),
            RunReport(rc,
                      {datetime(2023, 9, 1): 10.5,
                       datetime(2023, 9, 2): 15.7,
                       datetime(2023, 9, 3): 12.2,
                       },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1)]),
            RunReport(rc,
                      {datetime(2023, 9, 1): 10.5,
                       datetime(2023, 9, 3): 12.2,
                       datetime(2023, 9, 2): 15.7,
                       },
                      [Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1), Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1)])
        ]

        rc2 = cfg.RunConfig(si, cfg.MarketConfig([s1, s2], cfg.TimeFrame.D, cfg.date(2020, 1, 1),
                                                 cfg.date(2021, 1, 1)), cfg.StrategyConfig({"p1": 1, "p2": 3}))
        not_equal_rr_arr = [
            RunReport(rc2,
                      {datetime(2023, 9, 1): 10.5,
                       datetime(2023, 9, 3): 12.2,
                       datetime(2023, 9, 2): 15.7,
                       },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1)]),
            RunReport(rc, {datetime(2023, 9, 1): 10.1,
                           datetime(2023, 9, 3): 12.2,
                           datetime(2023, 9, 2): 15.7,
                           },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1)]),
            RunReport(rc, {datetime(2023, 9, 1): 10.5,
                           datetime(2023, 9, 4): 12.2,
                           datetime(2023, 9, 2): 15.7,
                           },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1)]),
            RunReport(rc, {datetime(2023, 9, 1): 10.5,
                           datetime(2023, 9, 3): 12.2,
                           datetime(2023, 9, 2): 15.7,
                           },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1)]),
            RunReport(rc, {datetime(2023, 9, 1): 10.5,
                           datetime(2023, 9, 3): 12.2,
                           datetime(2023, 9, 2): 15.7,
                           },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 2, datetime(2023, 9, 3), 2, 3,1)]),
            RunReport(rc, {datetime(2023, 9, 1): 10.5,
                           datetime(2023, 9, 3): 12.2,
                           datetime(2023, 9, 2): 15.7,
                           },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3, 1,-1)]),
            RunReport(rc, {datetime(2023, 9, 1): 10.5,
                           datetime(2023, 9, 3): 12.2,
                           datetime(2023, 9, 2): 15.7,
                           },
                      [Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,1), Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 4), 2, 3,1)])
        ]
        # Act

        # Assert
        for eq_rr in equal_rr_arr:
            self.assertEqual(hash(base_rr), hash(eq_rr), msg=eq_rr)
            self.assertEqual(base_rr, eq_rr, msg=eq_rr)

        for not_eq_rr in not_equal_rr_arr:
            self.assertNotEqual(hash(base_rr), hash(not_eq_rr), msg=not_eq_rr)
            self.assertNotEqual(base_rr, not_eq_rr, msg=not_eq_rr)
