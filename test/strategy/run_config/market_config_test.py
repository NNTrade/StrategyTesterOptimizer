import unittest
import logging
from src.strategy.run_config import MarketConfig, date


class MarketConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_init_with_single_stock_THEN_correct_stocks_tuple(self):
        # Array
        mc = MarketConfig(["S1"], date(2020, 1, 1), date(2021, 1, 1))

        # Act
        asserted_stocks = mc.stocks
        # Assert
        self.assertEqual(["S1"], asserted_stocks)

        asserted_to_list = [s for s in asserted_stocks]
        self.assertEqual(1, len(asserted_to_list))
        self.assertEqual(["S1"], asserted_to_list)

    def test_WHEN_init_with_multiple_stock_THEN_correct_stocks_tuple(self):
        # Array
        mc = MarketConfig(["S1", "S2"], date(2020, 1, 1), date(2021, 1, 1))

        # Act
        asserted_stocks = mc.stocks
        # Assert
        self.assertEqual(["S1", "S2"], asserted_stocks)

        asserted_to_list = [s for s in asserted_stocks]
        self.assertEqual(2, len(asserted_to_list))
        self.assertEqual(["S1", "S2"], asserted_to_list)

    def test_WHEN_check_that_from_LT_untill_THEN_error(self):
        # Array
        # Act

        # Assert
        with self.assertRaises(AttributeError) as context:
            rc = MarketConfig(["S1", "S2"], date(2021, 1, 2), date(2021, 1, 1))

        with self.assertRaises(AttributeError) as context:
            rc = MarketConfig(["S1", "S2"], date(2021, 1, 1), date(2021, 1, 1))

    def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
        # Array
        mc1 = MarketConfig(["A", "B"], date(2020, 1, 1),
                           date(2021, 1, 1))
        mc2 = MarketConfig(["A", "B"], date(2020, 1, 1),
                           date(2021, 1, 1))
        wrong_mc_arr = [
            MarketConfig(["A", "b"], date(2020, 1, 1),
                         date(2021, 1, 1)),
            MarketConfig(["A", "B"], date(2020, 1, 2),
                         date(2021, 1, 1)),
            MarketConfig(["A", "B"], date(2020, 1, 1),
                         date(2021, 1, 2)),
            MarketConfig(["A"], date(2020, 1, 1),
                         date(2021, 1, 1)),
            MarketConfig(["A", "B", "b"], date(2020, 1, 1),
                         date(2021, 1, 1))]
        # Act

        # Assert
        self.assertEqual(hash(mc1), hash(mc2))
        self.assertEqual(mc1, mc2)

        for wrong_rc in wrong_mc_arr:
            self.assertNotEqual(hash(mc1), hash(wrong_rc),
                                msg=wrong_rc)
            self.assertNotEqual(mc1, wrong_rc,
                                msg=wrong_rc)
