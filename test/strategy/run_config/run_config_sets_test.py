import unittest
import logging
from src.strategy.run_config import RunConfigSet, MarketConfigSet, StrategyConfigSet, date, StrategyId, StockConfig, TimeFrame, StrategyConfig
from src.strategy.run_config.is_valid_checker import IsValidChecker


class RunConfigSets_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    class TestIsValidChecker(IsValidChecker[StrategyConfig]):
        def is_valid(self, validation_object: StrategyConfig) -> bool:
            return validation_object != {"A": 2, "B": 4}
    def test_WHEN_build_records_THEN_get_correct_list(self):
        # Array
        s1 = StockConfig("S1", TimeFrame.D)
        s2 = StockConfig("S2", TimeFrame.D)
        s3 = StockConfig("S3", TimeFrame.D)
        si = StrategyId("test", "0.0.1")
        mcs = MarketConfigSet.Builder()\
            .add_stocks(["S1", "S2"], TimeFrame.D, date(2020, 1, 1), date(2021, 1, 1))\
            .add_stock("S3", TimeFrame.D, date(2022, 1, 1), date(2023, 1, 1))\
            .build()
        ivc = RunConfigSets_TestCase.TestIsValidChecker()
        scs = StrategyConfigSet.Builder().add_set(
            "A", [1, 2, 3]).add_set("B", [4, 5, 6]).add_is_valid_checker(ivc).build()
        rcs = RunConfigSet(si, mcs, scs)

        # Act
        asserted_list = rcs.as_records()

        # Assert
        self.assertEqual(16, len(asserted_list))

        i = 0
        self.assertEqual(si, asserted_list[i].strategy_id)
        self.assertEqual([s1, s2], asserted_list[i].market_cfg.stocks)
        self.assertEqual(date(2020, 1, 1),
                         asserted_list[i].market_cfg.from_date)
        self.assertEqual(date(2021, 1, 1),
                         asserted_list[i].market_cfg.untill_date)
        self.assertEqual({"A": 1, "B": 4},  asserted_list[i].strategy_cfg)

        i = 8
        self.assertEqual(si, asserted_list[i].strategy_id)
        self.assertEqual([s3], asserted_list[i].market_cfg.stocks)
        self.assertEqual(date(2022, 1, 1),
                         asserted_list[i].market_cfg.from_date)
        self.assertEqual(date(2023, 1, 1),
                         asserted_list[i].market_cfg.untill_date)
        self.assertEqual({"A": 1, "B": 4},  asserted_list[i].strategy_cfg)

    def test_WHEN_build_with_same_time_interval_THEN_get_correct_instance(self):
        # Array
        si = StrategyId("test", "0.0.1")
        s1 = StockConfig("S1", TimeFrame.D)
        s2 = StockConfig("S2", TimeFrame.D)
        rc = RunConfigSet(si, MarketConfigSet.Builder().add_stocks_set(
            [["S1"], ["S2"]], TimeFrame.D, date(2020, 1, 1), date(2021, 1, 1)).build())
        # Act
        assertedConfig = rc.market_cfg_set.as_records()

        # Assert
        self.assertEqual(2, len(assertedConfig))
        for idx, s in enumerate([[s1], [s2]]):
            assertedMarketSet = assertedConfig[idx]
            self.assertEqual(s, assertedMarketSet.stocks)
            self.assertEqual(date(2020, 1, 1), assertedMarketSet.from_date)
            self.assertEqual(date(2021, 1, 1), assertedMarketSet.untill_date)
