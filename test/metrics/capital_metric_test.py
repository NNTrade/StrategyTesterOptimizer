import unittest
import logging
from src.common.date_period import DatePeriod
from src.metrics.capital_metric import CapitalMetric, datetime, Deal, List, Dict, np


class CapitalMetric_CapitalLoading_Log_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_give_data_THEN_get_correct_result(self):
        # Array
        using_cap_log: Dict[datetime, float] = {
            datetime(2020, 1, 1): 100,
            datetime(2020, 1, 2): 110,
            datetime(2020, 1, 3): 250,
            datetime(2020, 1, 4): 430,
            datetime(2020, 1, 5): 230,
            datetime(2020, 1, 6): 230,
        }
        using_deal_log: List[Deal] = [
            Deal(datetime(2020, 1, 2), 10, 10, "A", 30, 0).set_last_price(
                datetime(2020, 1, 3), 20).close_deal(datetime(2020, 1, 4), 30),
            Deal(datetime(2020, 1, 3), 5, 5, "B", 30, 0).set_last_price(
                datetime(2020, 1, 4), 10).close_deal(datetime(2020, 1, 5), 20)
        ]

        expected_cap_load = {
            datetime(2020, 1, 1): 0,
            datetime(2020, 1, 2): 10*10/110,  # load by deal A
            datetime(2020, 1, 3): (10*20+5*5)/250,  # load by deal A+B
            datetime(2020, 1, 4): (10*30+10*5)/430,  # load by deal A+B
            datetime(2020, 1, 5): (20*5)/230,  # load by deal B
            datetime(2020, 1, 6): 0,
        }
        # Act
        asserted_cap_load = CapitalMetric.calc_capital_loading_log(
            using_cap_log, using_deal_log)

        # Assert
        self.assertEqual(len(asserted_cap_load), 6)
        for k, v in expected_cap_load.items():
            self.assertEqual(
                asserted_cap_load[k], v, msg=f"Load not equal on date {k}")

    def test_WHEN_if_deal_doesnt_has_price_on_date_THEN_attribute_excption(self):
        # Array
        using_cap_log: Dict[datetime, float] = {
            datetime(2020, 1, 1): 100,
            datetime(2020, 1, 2): 110,
            datetime(2020, 1, 3): 250,
            datetime(2020, 1, 4): 430,
            datetime(2020, 1, 5): 230,
            datetime(2020, 1, 6): 230,
        }
        using_deal_log: List[Deal] = [
            Deal(datetime(2020, 1, 2), 10, 10, "A", 30,
                 0).close_deal(datetime(2020, 1, 4), 30),
            Deal(datetime(2020, 1, 3), 5, 5, "B", 30, 0).set_last_price(
                datetime(2020, 1, 4), 10).close_deal(datetime(2020, 1, 5), 20)
        ]
        # Act

        # Assert
        with self.assertRaises(KeyError):
            CapitalMetric.calc_capital_loading_log(
                using_cap_log, using_deal_log)


class CapitalMetric_AvgCapitalLog_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_valus_THEN_correct_avg(self):
        # Array
        using_cap_log: Dict[datetime, float] = {
            datetime(2020, 1, 1): 100,
            datetime(2020, 1, 2): 110,
            datetime(2020, 1, 3): 250,
            datetime(2020, 1, 4): 430,
            datetime(2020, 1, 5): 230,
            datetime(2020, 1, 6): 230,
        }
        using_deal_log: List[Deal] = [
            Deal(datetime(2020, 1, 2), 10, 10, "A", 30, 0).set_last_price(
                datetime(2020, 1, 3), 20).close_deal(datetime(2020, 1, 4), 30),
            Deal(datetime(2020, 1, 3), 5, 5, "B", 30, 0).set_last_price(
                datetime(2020, 1, 4), 10).close_deal(datetime(2020, 1, 5), 20)
        ]

        expected_avg_cap_load = np.mean([
            0,
            10*10/110,  # load by deal A
            (10*20+5*5)/250,  # load by deal A+B
            (10*30+10*5)/430,  # load by deal A+B
            (20*5)/230,  # load by deal B
            0,
        ])

        # Act
        asserted_avg_cap_load = CapitalMetric(DatePeriod(
            datetime(2020, 1, 1), datetime(2020, 1, 7)), using_cap_log, using_deal_log).avg_loading

        # Assert
        self.assertEqual(asserted_avg_cap_load, expected_avg_cap_load)
