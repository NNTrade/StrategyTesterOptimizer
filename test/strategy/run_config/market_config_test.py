import unittest
import logging
from src.strategy.run_config import MarketConfig, date, StockConfig, TimeFrame, timedelta


class MarketConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_init_with_single_stock_THEN_correct_stocks_tuple(self):
        # Array
        s1 = StockConfig("S1", TimeFrame.D)
        mc = MarketConfig([s1], TimeFrame.D, date(
            2020, 1, 1), date(2021, 1, 1))

        # Act
        asserted_stocks = mc.stocks
        # Assert
        self.assertEqual([s1], asserted_stocks)

        asserted_to_list = [s for s in asserted_stocks]
        self.assertEqual(1, len(asserted_to_list))
        self.assertEqual([s1], asserted_to_list)

    def test_WHEN_init_with_multiple_stock_THEN_correct_stocks_tuple(self):
        # Array
        s1 = StockConfig("S1", TimeFrame.D)
        s2 = StockConfig("S2", TimeFrame.D)
        mc = MarketConfig([s1, s2], TimeFrame.D, date(
            2020, 1, 1), date(2021, 1, 1))

        # Act
        asserted_stocks = mc.stocks
        # Assert
        self.assertEqual([s1, s2], asserted_stocks)

        asserted_to_list = [s for s in asserted_stocks]
        self.assertEqual(2, len(asserted_to_list))
        self.assertEqual([s1, s2], asserted_to_list)

    def test_WHEN_request_period_in_years_THEN_get_correct_unsver(self):
        # Array
        s1 = StockConfig("S1", TimeFrame.D)
        s2 = StockConfig("S2", TimeFrame.D)
        mc = MarketConfig([s1, s2], TimeFrame.D, date(
            2020, 1, 1), date(2021, 1, 1))
        # Act
    
        # Assert
        self.assertEqual(366, mc.period_in_days)
        self.assertAlmostEquals(366/365, mc.period_in_years,5)

    def test_WHEN_check_that_from_LT_untill_THEN_error(self):
        # Array
        # Act

        # Assert
        s1 = StockConfig("S1", TimeFrame.D)
        s2 = StockConfig("S2", TimeFrame.D)
        with self.assertRaises(AttributeError) as context:
            rc = MarketConfig([s1, s2], TimeFrame.D, date(
                2021, 1, 2), date(2021, 1, 1))

        with self.assertRaises(AttributeError) as context:
            rc = MarketConfig([s1, s2], TimeFrame.D, date(
                2021, 1, 1), date(2021, 1, 1))

    def test_WHEN_check_that_step_tf_LE_stock_tf_THEN_error(self):
        # Array
        # Act

        # Assert
        s1 = StockConfig("S1", TimeFrame.W)
        s2 = StockConfig("S2", TimeFrame.D)
        MarketConfig([s1, s2], TimeFrame.m1, date(
            2020, 1, 2), date(2021, 1, 1))
        with self.assertRaises(AttributeError) as context:
            rc = MarketConfig([s1, s2], TimeFrame.W, date(
                2020, 1, 2), date(2021, 1, 1))

        with self.assertRaises(AttributeError) as context:
            rc = MarketConfig([s1, s2], TimeFrame.M, date(
                2020, 1, 1), date(2021, 1, 1))

    def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        s2 = StockConfig("B", TimeFrame.D)
        mc1 = MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                           date(2021, 1, 1))
        eq_mc_arr = [
            MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                         date(2021, 1, 1)),
            MarketConfig([s1, s2], TimeFrame.DAY, date(2020, 1, 1),
                         date(2021, 1, 1)),
            MarketConfig([s2, s1], TimeFrame.D, date(2020, 1, 1),
                         date(2021, 1, 1))
        ]

        s3 = StockConfig("b", TimeFrame.D)
        wrong_mc_arr = [
            MarketConfig([s1, s3], TimeFrame.D, date(2020, 1, 1),
                         date(2021, 1, 1)),
            MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 2),
                         date(2021, 1, 1)),
            MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                         date(2021, 1, 2)),
            MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                         date(2021, 1, 1)),
            MarketConfig([s1, s2, s3], TimeFrame.D, date(2020, 1, 1),
                         date(2021, 1, 1)),
            MarketConfig([s1, s2], TimeFrame.m1, date(2020, 1, 1),
                         date(2021, 1, 1))]
        # Act

        # Assert
        for asserted_mc in eq_mc_arr:
            self.assertEqual(hash(mc1), hash(asserted_mc),msg=asserted_mc)
            self.assertEqual(mc1, asserted_mc,msg=asserted_mc)

        for wrong_rc in wrong_mc_arr:
            self.assertNotEqual(hash(mc1), hash(wrong_rc),
                                msg=wrong_rc)
            self.assertNotEqual(mc1, wrong_rc,
                                msg=wrong_rc)

    def test_WHEN_split_sharp_THEN_correct_splitting(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 11))
        expected_list = [
            MarketConfig([s1], TimeFrame.D, date(
                2020, 1, 1), date(2020, 1, 3)),
            MarketConfig([s1], TimeFrame.D, date(
                2020, 1, 3), date(2020, 1, 5)),
            MarketConfig([s1], TimeFrame.D, date(
                2020, 1, 5), date(2020, 1, 7)),
            MarketConfig([s1], TimeFrame.D, date(
                2020, 1, 7), date(2020, 1, 9)),
            MarketConfig([s1], TimeFrame.D, date(
                2020, 1, 9), date(2020, 1, 11)),
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
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 11))
        expected_list = [
            MarketConfig([s1], TimeFrame.D, date(
                2020, 1, 1), date(2020, 1, 4)),
            MarketConfig([s1], TimeFrame.D, date(
                2020, 1, 4), date(2020, 1, 7)),
            MarketConfig([s1], TimeFrame.D, date(
                2020, 1, 7), date(2020, 1, 11))
        ]
        used_chuck_count = 3
        # Act
        asserted_list = mc1.split(used_chuck_count)

        # Assert
        self.assertEqual(used_chuck_count, len(asserted_list))
        for i in range(used_chuck_count):
            self.assertEqual(expected_list[i], asserted_list[i])


class MarketConfig_Split_On_Optiomization_Chunks_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                                datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_give_wrong_intervals_THEN_get_errors(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 11))
        
        # Act

        # Assert
        with self.assertRaises(AttributeError) as context:
            mc1.split_on_opt_chunks(timedelta(1),timedelta(1))
                                    
        with self.assertRaises(AttributeError) as context:
            mc1.split_on_opt_chunks(timedelta(3,hours=23),timedelta(1))
        
        with self.assertRaises(AttributeError) as context:
            mc1.split_on_opt_chunks(timedelta(8,1),timedelta(1))

        with self.assertRaises(AttributeError) as context:
            mc1.split_on_opt_chunks(timedelta(10),timedelta(1))

    def test_WHEN_forced_split_THEN_no_check_interval_relations(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 12))
        
        # Act

        # Assert
        mc1.split_on_opt_chunks(timedelta(1),timedelta(1), True)
                                    
        mc1.split_on_opt_chunks(timedelta(3,hours=23),timedelta(1), True,True)
        
        mc1.split_on_opt_chunks(timedelta(8,1),timedelta(1), True)

        mc1.split_on_opt_chunks(timedelta(10),timedelta(1), True)


    def test_WHEN_split_THEN_split_correct(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 10))
        expected_intervals = [
            ((date(2020, 1, 1), date(2020, 1, 5)),(date(2020, 1, 5), date(2020, 1, 6)) ),
            ((date(2020, 1, 2), date(2020, 1, 6)),(date(2020, 1, 6), date(2020, 1, 7)) ),
            ((date(2020, 1, 3), date(2020, 1, 7)),(date(2020, 1, 7), date(2020, 1, 8)) ),
            ((date(2020, 1, 4), date(2020, 1, 8)),(date(2020, 1, 8), date(2020, 1, 9)) ),
            ((date(2020, 1, 5), date(2020, 1, 9)),(date(2020, 1, 9), date(2020, 1, 10)) ),
        ]
        # Act
        asserted_tuples = mc1.split_on_opt_chunks(timedelta(4),timedelta(1))

        # Assert
        self.assertEqual(5, len(asserted_tuples))
        for idx,expected_interval in enumerate(expected_intervals):
            expected_mc1 = MarketConfig([s1], TimeFrame.D, expected_interval[0][0], expected_interval[0][1])
            expected_mc2 = MarketConfig([s1], TimeFrame.D, expected_interval[1][0], expected_interval[1][1])
            self.assertEqual(expected_mc1, asserted_tuples[idx][0])
            self.assertEqual(expected_mc2, asserted_tuples[idx][1])

    def test_WHEN_split_with_tail_THEN_raise_error(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 14))
        expected_intervals = [
            ((date(2020, 1, 1), date(2020, 1, 9)),(date(2020, 1, 9), date(2020, 1, 11)) ),
            ((date(2020, 1, 3), date(2020, 1, 11)),(date(2020, 1, 11), date(2020, 1, 13)) ),
        ]
        # Act
        # Assert
        with self.assertRaises(AttributeError) as context:
            mc1.split_on_opt_chunks(timedelta(8),timedelta(2))

    def test_WHEN_split_with_cut_tail_THEN_raise_error(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 14))
        expected_intervals = [
            ((date(2020, 1, 1), date(2020, 1, 9)),(date(2020, 1, 9), date(2020, 1, 11)) ),
            ((date(2020, 1, 3), date(2020, 1, 11)),(date(2020, 1, 11), date(2020, 1, 13)) ),
        ]
        # Act
        asserted_tuples = mc1.split_on_opt_chunks(timedelta(8),timedelta(2), cut_tail=True)

        # Assert
        self.assertEqual(2, len(asserted_tuples))
        for idx,expected_interval in enumerate(expected_intervals):
            expected_mc1 = MarketConfig([s1], TimeFrame.D, expected_interval[0][0], expected_interval[0][1])
            expected_mc2 = MarketConfig([s1], TimeFrame.D, expected_interval[1][0], expected_interval[1][1])
            self.assertEqual(expected_mc1, asserted_tuples[idx][0])
            self.assertEqual(expected_mc2, asserted_tuples[idx][1])

    def test_WHEN_cannt_split_THEN_return_empty(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 5))
        # Act
        asserted_tuples = mc1.split_on_opt_chunks(timedelta(8),timedelta(1), cut_tail=True)
        
        # Assert
        self.assertEqual(0, len(asserted_tuples))
            
                                    