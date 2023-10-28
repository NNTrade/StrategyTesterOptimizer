import unittest
import logging
from src.strategy.run_config import RunConfigSet, MarketConfigSets, StrategyConfigSets, date


class RunConfigSets_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_build_records_THEN_get_correct_list(self):
        # Array
        mcs = MarketConfigSets.Builder()\
            .add_stocks(["S1", "S2"], date(2020, 1, 1), date(2021, 1, 1))\
            .add_stock("S3", date(2022, 1, 1), date(2023, 1, 1))\
            .build()
        scs = StrategyConfigSets.Builder().add_set(
            "A", [1, 2, 3]).add_set("B", [4, 5, 6]).add_validation_func(lambda rec: rec != {"A": 2, "B": 4}).build()
        rcs = RunConfigSet(mcs, scs)

        # Act
        asserted_list = rcs.as_records()

        # Assert
        self.assertEqual(16, len(asserted_list))

        i = 0
        self.assertEqual(["S1", "S2"], asserted_list[i].market_cfg.stocks)
        self.assertEqual(date(2020, 1, 1),
                         asserted_list[i].market_cfg.from_date)
        self.assertEqual(date(2021, 1, 1),
                         asserted_list[i].market_cfg.untill_date)
        self.assertEqual({"A": 1, "B": 4},  asserted_list[i].strategy_cfg)

        i = 8
        self.assertEqual(["S3"], asserted_list[i].market_cfg.stocks)
        self.assertEqual(date(2022, 1, 1),
                         asserted_list[i].market_cfg.from_date)
        self.assertEqual(date(2023, 1, 1),
                         asserted_list[i].market_cfg.untill_date)
        self.assertEqual({"A": 1, "B": 4},  asserted_list[i].strategy_cfg)

    def test_WHEN_build_with_same_time_interval_THEN_get_correct_instance(self):
        # Array
        rc = RunConfigSet(MarketConfigSets.Builder().add_stocks_set(
            [["s1"], ["s2"]], date(2020, 1, 1), date(2021, 1, 1)).build())
        # Act
        assertedConfig = rc.market_cfg_set.as_records()

        # Assert
        self.assertEqual(2, len(assertedConfig))
        for idx, s in enumerate([["s1"], ["s2"]]):
            assertedMarketSet = assertedConfig[idx]
            self.assertEqual(s, assertedMarketSet.stocks)
            self.assertEqual(date(2020, 1, 1), assertedMarketSet.from_date)
            self.assertEqual(date(2021, 1, 1), assertedMarketSet.untill_date)
