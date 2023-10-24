from dataclasses import FrozenInstanceError
import unittest
import logging
from src.strategy.run_config import RunConfig, date


class RunConfig_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_construct_THEN_construct_correctly(self):
    # Array
    rc = RunConfig(["A", "B"], date(2020, 1, 1),
                   date(2021, 1, 1), {"p1": 1, "p2": 2})
    # Act

    # Assert
    self.assertEqual(2, len(rc.stock_list))
    self.assertIn("A", rc.stock_list)
    self.assertIn("B", rc.stock_list)
    self.assertEqual(date(2020, 1, 1), rc.from_date)
    self.assertEqual(date(2021, 1, 1), rc.till_date)
    self.assertEqual(2, len(rc.parameters.keys()))
    self.assertEqual(1, rc.parameters["p1"])
    self.assertEqual(2, rc.parameters["p2"])

  def test_WHEN_construct_THEN_it_is_imutable(self):
    # Array
    rc = RunConfig(["A", "B"], date(2020, 1, 1),
                   date(2021, 1, 1), {"p1": 1, "p2": 2})

    # Act
    with self.assertRaises(AttributeError):
      rc.stock_list.append("C")
    with self.assertRaises(AttributeError):
      rc.stock_list = ['C']
    with self.assertRaises(AttributeError):
      rc.from_date = date(2020, 1, 2)
    with self.assertRaises(AttributeError):
      rc.till_date = date(2021, 1, 2)
    with self.assertRaises(TypeError):
      rc.parameters["p1"] = 2
    with self.assertRaises(AttributeError):
      rc.parameters = {"p3": 3}

    # Assert
    self.assertEqual(2, len(rc.stock_list))
    self.assertIn("A", rc.stock_list)
    self.assertIn("B", rc.stock_list)
    self.assertEqual(date(2020, 1, 1), rc.from_date)
    self.assertEqual(date(2021, 1, 1), rc.till_date)
    self.assertEqual(2, len(rc.parameters.keys()))
    self.assertEqual(1, rc.parameters["p1"])
    self.assertEqual(2, rc.parameters["p2"])


  def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
    # Array
    rc1 = RunConfig(["A", "B"], date(2020, 1, 1),
                    date(2021, 1, 1), {"p1": 1, "p2": 2})
    rc2 = RunConfig(["A", "B"], date(2020, 1, 1),
                    date(2021, 1, 1), {"p1": 1, "p2": 2})
    # Act

    # Assert
    self.assertEqual(hash(rc1), hash(rc2))
    self.assertEqual(rc1, rc2)
