from datetime import datetime
import unittest
import logging
from src.simulation.models import SimulationLog
from src.models.deal import Deal
class Simulation_Log_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_serialization_and_deserialization_THEN_equals(self):
        # Array
               
        expected_cfg = SimulationLog(
            {datetime(2020,1,day,10,12,3):day*1.3 for day in range(1,10)},
            [
                Deal(datetime(2020,1,2,10,12,3), 1.2, 10,"A",0.2, -1.2).add_commision_holding(-10),
                Deal(datetime(2020,1,4,10,12,3), 2.2, 11,"B",1.2, -2.2).close_deal(datetime(2020,1,5,10,12,3), 1.2, -0.1)
            ])

        # Act
        json_str = expected_cfg.to_json()

        # Parse the JSON back into a DTO
        asserted_cfg = SimulationLog.from_json(json_str)
        
        # Assert
        self.assertEqual(expected_cfg, asserted_cfg)