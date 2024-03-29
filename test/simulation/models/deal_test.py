import unittest
import logging
from src.simulation.models.deal import Deal, datetime


class Deal_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_compore_THEN_correct_result(self):
        # Array
        base_d = Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -1)
        eq_d_arr = [
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -1)
        ]
        not_eq_d_arr = [
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -1).add_commision_holding(3),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -1).close_deal(datetime(2020,1,2), 3),
            Deal(datetime(2020, 1, 2), 10, 100, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 11, 100, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 101, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "B", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.4, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -3),
        ]
        # Act

        # Assert
        print(base_d)

        for d in eq_d_arr:
            self.assertEqual(hash(base_d), hash(d), msg=d)
            self.assertEqual(base_d, d, msg=d)

        for d in not_eq_d_arr:
            self.assertNotEqual(hash(base_d), hash(d), msg=d)
            self.assertNotEqual(base_d, d, msg=d)

    def test_WHEN_request_result_or_profit_THEN_correct(self):
        # Array
        used_d = Deal(datetime(2020, 1, 1), 10, 100, "A", 0.5, -1).add_commision_holding(2).add_commision_holding(1).close_deal(datetime(2020,2,2), 11, -2)
       
        # Act
        asserted_result = used_d.result
        asserted_profit = used_d.profit

        # Assert    
        self.assertEqual((11 - 10)*100 - 1 + 3 - 2, asserted_result)
        self.assertEqual(100 / (10*100/0.5), asserted_profit)

    def test_WHEN_serialization_and_deserialization_THEN_equals(self):
        # Array        
        expected_cfg = Deal(datetime(2020,1,2,10,12,3), 1.2, 10,"A",0.2, -1.2)

        # Act
        json_str = expected_cfg.to_json()

        # Parse the JSON back into a DTO
        asserted_cfg = Deal.from_json(json_str)
        
        # Assert
        self.assertEqual(expected_cfg, asserted_cfg)

    def test_WHEN_open_with_commision_serialization_and_deserialization_THEN_equals(self):
        # Array        
        expected_cfg = Deal(datetime(2020,1,2,10,12,3), 1.2, 10,"A",0.2, -1.2)
        expected_cfg.add_commision_holding(10)

        # Act
        json_str = expected_cfg.to_json()

        # Parse the JSON back into a DTO
        asserted_cfg = Deal.from_json(json_str)
        
        # Assert
        self.assertEqual(expected_cfg, asserted_cfg)

    def test_WHEN_closed_serialization_and_deserialization_THEN_equals(self):
        # Array        
        expected_cfg = Deal(datetime(2020,1,2,10,12,3), 1.2, 10,"A",0.2, -1.2)
        expected_cfg.add_commision_holding(10)
        expected_cfg.close_deal(datetime(2020,1,3,10,12,3),2,-0.8)

        # Act
        json_str = expected_cfg.to_json()

        # Parse the JSON back into a DTO
        asserted_cfg = Deal.from_json(json_str)
        
        # Assert
        self.assertEqual(expected_cfg, asserted_cfg)