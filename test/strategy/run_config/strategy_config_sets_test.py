import unittest
import logging
from src.strategy.run_config.is_valid_checker import IsValidChecker
from src.strategy.run_config.strategy_config_sets import StrategyConfigSet, StrategyConfig


class ParametersSets_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  
  class TestIsValidChecker(IsValidChecker[StrategyConfig]):
    def is_valid(self, validation_object: StrategyConfig) -> bool:
        return validation_object != {"A": 2, "B": 4}
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
      ivc = ParametersSets_TestCase.TestIsValidChecker()
      ps = StrategyConfigSet.Builder().add_set("A", [1, 2, 3]).add_set(
          "B", [4, 5, 6]).add_is_valid_checker(ivc).build()

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

  def test_WHEN_get_records_THEN_it_created_use_startegy_config(self):
      # Array
      str_set = StrategyConfigSet.Builder().add_set("A", [1,2]).add_set(
          "B", [4]).build()
      expected_record1 = StrategyConfig({"A":1, "B":4})
      expected_record2 = StrategyConfig({"A":2, "B":4})

      # Act
      asserted_records = str_set.as_records()
      
      # Assert
      for assert_rec in asserted_records:
        hash(assert_rec)
      self.assertEqual(2, len(asserted_records))
      self.assertIn(expected_record1, asserted_records)
      self.assertIn(expected_record2, asserted_records)
