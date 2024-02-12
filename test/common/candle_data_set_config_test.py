import unittest
import logging
from src.common import CandleDataSetConfig,TimeFrame,CandleConfig


class CandleDataSetConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_init_with_single_stock_THEN_correct_stocks_tuple(self):
        # Array
        s1 = CandleConfig("S1", TimeFrame.D)
        mc = CandleDataSetConfig.BuildFromList([s1], TimeFrame.D)

        # Act
        asserted_stocks = mc.stocks
        # Assert

        self.assertEqual(1, len(asserted_stocks))
        self.assertEqual(s1, asserted_stocks["0"])

    def test_WHEN_init_stocks_from_list_THEN_correct_stocks_tuple(self):
        # Array
        s1 = CandleConfig("S1", TimeFrame.D)
        s2 = CandleConfig("S2", TimeFrame.D)
        mc = CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D)

        # Act
        asserted_stocks = mc.stocks
        # Assert
        self.assertEqual(s1, asserted_stocks["0"])
        self.assertEqual(s2, asserted_stocks["1"])
        
    def test_WHEN_init_stocks_from_dict_THEN_correct_stocks_tuple(self):
        # Array
        s1 = CandleConfig("S1", TimeFrame.D)
        s2 = CandleConfig("S2", TimeFrame.D)
        mc = CandleDataSetConfig.BuildFromDict({"A":s1,"B":s2}, TimeFrame.D)

        # Act
        asserted_stocks = mc.stocks
        # Assert
        self.assertEqual(s1, asserted_stocks["A"])
        self.assertEqual(s2, asserted_stocks["B"])

    def test_WHEN_check_that_step_tf_LE_stock_tf_THEN_error(self):
        # Array
        # Act

        # Assert
        s1 = CandleConfig("S1", TimeFrame.W)
        s2 = CandleConfig("S2", TimeFrame.D)
        CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.m1)
        with self.assertRaises(AttributeError) as context:
            rc = CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.W)

        with self.assertRaises(AttributeError) as context:
            rc = CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.M)

    def test_WHEN_change_stock_config_order_THEN_not_equal(self):
        # Array
        s1 = CandleConfig("A", TimeFrame.D)
        s2 = CandleConfig("B", TimeFrame.D)
        mc1 = CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D)
        asserted_mc2 = CandleDataSetConfig.BuildFromList([s2, s1], TimeFrame.D)
        # Act
  
        # Assert
        self.assertNotEqual(hash(mc1), hash(asserted_mc2))
        self.assertNotEqual(mc1, asserted_mc2)

    def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
        # Array
        s1 = CandleConfig("A", TimeFrame.D)
        s2 = CandleConfig("B", TimeFrame.D)
        mc1 = CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D)
        eq_mc_arr = [
            CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.D),
            CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.DAY),            
        ]

        s3 = CandleConfig("b", TimeFrame.D)
        wrong_mc_arr = [
            CandleDataSetConfig.BuildFromList([s1, s3], TimeFrame.D),
            CandleDataSetConfig.BuildFromList([s1], TimeFrame.D),
            CandleDataSetConfig.BuildFromList([s1, s2, s3], TimeFrame.D),
            CandleDataSetConfig.BuildFromList([s1, s2], TimeFrame.m1)]
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
            