import unittest
import logging
from src.common.candle_config import CandleConfig, TimeFrame

class CandleConfig_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_serialize_and_desetrialize_by_json_THEN_equal(self):
    # Array
    expected_cfg = CandleConfig("A", TimeFrame.D)

    # Act
    json_str = expected_cfg.to_json()

    # Parse the JSON back into a DTO
    asserted_cfg = CandleConfig.from_json(json_str)
    
    # Assert
    self.assertEqual(expected_cfg, asserted_cfg)