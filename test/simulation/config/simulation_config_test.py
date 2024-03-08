import unittest
import logging
from src.common.candle_data_set_config import CandleDataSetConfig
from src.common.date_period import DatePeriod,date
from src.simulation.config import SimulationConfig, StrategyConfig, StrategyId, CandleConfig, TimeFrame

class SimulationConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_construct_THEN_construct_correctly(self):
        # Array
        s1 = CandleConfig("A", TimeFrame.D)
        s2 = CandleConfig("B", TimeFrame.D)
        c_ds_cfg = CandleDataSetConfig.BuildFromDict({"A":s1, "B":s2}, TimeFrame.D)
        dp = DatePeriod(date(2020, 1, 1), date(2021, 1, 1))
        rc = SimulationConfig(c_ds_cfg, dp, StrategyConfig({"p1": 1, "p2": 2}))
        # Act

        # Assert
        self.assertEqual(2, len(rc.candle_ds_cfg.stocks))
        self.assertEqual(s1, rc.candle_ds_cfg.stocks["A"])
        self.assertEqual(s2, rc.candle_ds_cfg.stocks["B"])
        self.assertEqual(date(2020, 1, 1), rc.period.from_date)
        self.assertEqual(date(2021, 1, 1), rc.period.untill_date)
        self.assertEqual(2, len(rc.strategy_cfg.keys()))
        self.assertEqual(1, rc.strategy_cfg["p1"])
        self.assertEqual(2, rc.strategy_cfg["p2"])

    def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
        # Array\
        s1 = CandleConfig("A", TimeFrame.D)
        s2 = CandleConfig("B", TimeFrame.D)
        c_ds_cfg = CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D)
        dp = DatePeriod(date(2020, 1, 1), date(2021, 1, 1))
        rc1 = SimulationConfig(c_ds_cfg, dp, StrategyConfig({"p1": 1, "p2": 2}))
        rc2 = SimulationConfig(c_ds_cfg, dp, StrategyConfig({"p1": 1, "p2": 2}))

        s3 = CandleConfig("b", TimeFrame.D)
        wrong_rc_arr = [
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.m1), DatePeriod(date(2020, 1, 1),
                                   date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s3], TimeFrame.D),  DatePeriod(date(2020, 1, 1),
                                   date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D),  DatePeriod(date(2020, 1, 2),
                                   date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D),  DatePeriod(date(2020, 1, 1),
                                   date(2021, 1, 2)), StrategyConfig({"p1": 1, "p2": 2})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D),  DatePeriod(date(2020, 1, 1),
                                   date(2021, 1, 1)), StrategyConfig({"P1": 1, "p2": 2})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D),  DatePeriod(date(2020, 1, 1),
                                   date(2021, 1, 1)), StrategyConfig({"p1": 2, "p2": 2})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D),  DatePeriod(date(2020, 1, 1),
                                   date(2021, 1, 1)), StrategyConfig({"p1": 1})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D),  DatePeriod(date(2020, 1, 1),
                                   date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2, "p3": 3})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1], TimeFrame.D),  DatePeriod(date(2020, 1, 1),
                                   date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            SimulationConfig(CandleDataSetConfig.BuildFromList([s1, s2, s3], TimeFrame.D),  DatePeriod(date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))]
        # Act

        # Assert
        self.assertEqual(hash(rc1), hash(rc2))
        self.assertEqual(rc1, rc2)

        for wrong_rc in wrong_rc_arr:
            self.assertNotEqual(hash(rc1), hash(wrong_rc),
                                msg=wrong_rc)
            self.assertNotEqual(rc1, wrong_rc)

    
    def test_WHEN_check_that_from_LT_untill_THEN_error(self):
        # Array
        # Act

        # Assert
        s1 = CandleConfig("S1", TimeFrame.D)
        s2 = CandleConfig("S2", TimeFrame.D)
        cds_cfg = CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D)
        with self.assertRaises(AttributeError) as context:
            rc = SimulationConfig(cds_cfg,DatePeriod(date(
                2021, 1, 2), date(2021, 1, 1)))

        with self.assertRaises(AttributeError) as context:
            rc = SimulationConfig(cds_cfg,DatePeriod(date(
                2021, 1, 1), date(2021, 1, 1)))
            
    def test_WHEN_split_sharp_THEN_correct_splitting(self):
        # Array
        s1 = CandleConfig("A", TimeFrame.D)
        cds_cfg = CandleDataSetConfig.BuildFromList([s1], TimeFrame.D)
        mc1 = SimulationConfig(cds_cfg,DatePeriod(date(2020, 1, 1),
                           date(2020, 1, 11)))
        expected_list = [
            SimulationConfig(cds_cfg,DatePeriod(date(
                2020, 1, 1), date(2020, 1, 3))),
            SimulationConfig(cds_cfg,DatePeriod(date(
                2020, 1, 3), date(2020, 1, 5))),
            SimulationConfig(cds_cfg,DatePeriod(date(
                2020, 1, 5), date(2020, 1, 7))),
            SimulationConfig(cds_cfg,DatePeriod(date(
                2020, 1, 7), date(2020, 1, 9))),
            SimulationConfig(cds_cfg,DatePeriod(date(
                2020, 1, 9), date(2020, 1, 11))),
        ]

        used_chuck_count = 5
        # Act

        asserted_list = mc1.split(used_chuck_count)

        # Assert
        self.assertEqual(used_chuck_count, len(asserted_list))
        for i in range(used_chuck_count):
            self.assertEqual(expected_list[i], asserted_list[i])

    def test_WHEN_split_near_THEN_correct_splitting(self):
        # Array
        s1 = CandleConfig("A", TimeFrame.D)
        cds_cfg = CandleDataSetConfig.BuildFromList([s1], TimeFrame.D)
        mc1 = SimulationConfig(cds_cfg,DatePeriod(date(2020, 1, 1),
                           date(2020, 1, 11)))
        expected_list = [
            SimulationConfig(cds_cfg,DatePeriod(date(
                2020, 1, 1), date(2020, 1, 4))),
            SimulationConfig(cds_cfg,DatePeriod(date(
                2020, 1, 4), date(2020, 1, 7))),
            SimulationConfig(cds_cfg,DatePeriod(date(
                2020, 1, 7), date(2020, 1, 11)))
        ]
        used_chuck_count = 3
        # Act
        asserted_list = mc1.split(used_chuck_count)

        # Assert
        self.assertEqual(used_chuck_count, len(asserted_list))
        for i in range(used_chuck_count):
            self.assertEqual(expected_list[i], asserted_list[i])

    def test_WHEN_serialization_and_deserialization_THEN_equals(self):
        # Array
        s1 = CandleConfig("A", TimeFrame.D)
        s2 = CandleConfig("B", TimeFrame.D)
        c_ds_cfg = CandleDataSetConfig.BuildFromDict({"A":s1, "B":s2}, TimeFrame.D)
        dp = DatePeriod(date(2020, 1, 1), date(2021, 1, 1))        
        expected_cfg = SimulationConfig(c_ds_cfg, dp, StrategyConfig({"p1": 1, "p2": 2.2, "p3":"1q2w3e"}))

        # Act
        json_str = expected_cfg.to_json()

        # Parse the JSON back into a DTO
        asserted_cfg = SimulationConfig.from_json(json_str)
        
        # Assert
        self.assertEqual(expected_cfg, asserted_cfg)
