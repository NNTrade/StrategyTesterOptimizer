import unittest
import logging
from src.strategy.run_config.strategy_config_sets import StrategyConfigSet


class ParametersSets_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_create_instance_THEN_work_like_dictionary(self):
    # Array
    ps = StrategyConfigSet.Builder().add_set(
        "A", [1, 2, 3]).add_set("B", [4, 5, 6]).build()

    # Act

    asserted_records = ps.as_records()

    # Assert
    self.assertEqual([1, 2, 3], ps["A"])

    self.assertEqual(9, len(asserted_records))

    self.assertEqual({"A": 1, "B": 4}, asserted_records[0])
    self.assertEqual({"A": 1, "B": 5}, asserted_records[1])
    self.assertEqual({"A": 1, "B": 6}, asserted_records[2])

    self.assertEqual({"A": 2, "B": 4}, asserted_records[3])
    self.assertEqual({"A": 2, "B": 5}, asserted_records[4])
    self.assertEqual({"A": 2, "B": 6}, asserted_records[5])

    self.assertEqual({"A": 3, "B": 4}, asserted_records[6])
    self.assertEqual({"A": 3, "B": 5}, asserted_records[7])
    self.assertEqual({"A": 3, "B": 6}, asserted_records[8])

  def test_WHEN_add_validation_func_THEN_records_contained_only_valid(self):
      # Array
      ps = StrategyConfigSet.Builder().add_set("A", [1, 2, 3]).add_set(
          "B", [4, 5, 6]).add_is_valid_func(lambda rec: rec != {"A": 2, "B": 4}).build()

      # Act

      asserted_records = ps.as_records()

      # Assert
      self.assertEqual(8, len(asserted_records))

      self.assertEqual({"A": 1, "B": 4}, asserted_records[0])
      self.assertEqual({"A": 1, "B": 5}, asserted_records[1])
      self.assertEqual({"A": 1, "B": 6}, asserted_records[2])

      # self.assertEqual({"A": 2, "B": 4}, asserted_records[3])
      self.assertEqual({"A": 2, "B": 5}, asserted_records[3])
      self.assertEqual({"A": 2, "B": 6}, asserted_records[4])

      self.assertEqual({"A": 3, "B": 4}, asserted_records[5])
      self.assertEqual({"A": 3, "B": 5}, asserted_records[6])
      self.assertEqual({"A": 3, "B": 6}, asserted_records[7])

  def test_WHEN_constructor_has_no_parameters_THEN_ok_and_records_is_empty(self):
      # Array
      ps = StrategyConfigSet()

      # Act
      asserted_records = ps.as_records()

      # Assert
      self.assertEqual(0, len(asserted_records))
