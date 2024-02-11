import unittest
import logging
from src.simulation.config import StrategyConfig


class StrategyConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
        # Array
        sc1 = StrategyConfig({"p1": 1, "p2": 2})
        sc2 = StrategyConfig({"p1": 1, "p2": 2})
        wrong_rc_arr = [
            StrategyConfig({"p1": 2, "p2": 2}),
            StrategyConfig({"p1": 1}),
            StrategyConfig({"p1": 1, "p2": 2, "p3": 3}),
            StrategyConfig({"p3": 1, "p2": 2})]
        # Act

        # Assert
        self.assertEqual(hash(sc1), hash(sc2))
        self.assertEqual(sc1, sc2)

        for wrong_rc in wrong_rc_arr:
            self.assertNotEqual(hash(sc1), hash(wrong_rc),
                                msg=wrong_rc)
            self.assertNotEqual(sc1, wrong_rc)