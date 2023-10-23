import unittest
import logging
from src.strategy.run_config import RunConfig


class RunConfig_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_construct_THEN_construct_correctly(self):
    # Array

    # Act

    # Assert

  def test_WHEN_construct_THEN_it_is_imutable(self):
    # Array

    # Act

    # Assert

  def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
    # Array

    # Act

    # Assert
