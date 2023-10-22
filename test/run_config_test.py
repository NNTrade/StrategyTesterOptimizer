import unittest
import logging
from src.run_config import RunConfig, date


class RunConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_build_with_same_time_interval_THEN_get_correct_instance(self):
        # Array
        rc = RunConfig.buildSameTradeInterval(
            ["s1", "s2"], date(2020, 1, 1), date(2021, 1, 1))
        # Act
        assertedConfig = rc.stocks

        # Assert
        self.assertEqual(2, len(assertedConfig))
        for s in ["s1", "s2"]:
            assertedPeriod = assertedConfig[s]
            self.assertEqual(date(2020, 1, 1), assertedPeriod[0])
            self.assertEqual(date(2021, 1, 1), assertedPeriod[1])

    def test_WHEN_build_with_different_interval_THEN_get_correct_instance(self):
        # Array
        expectedConfig = {
            "s1": (date(2020, 1, 1), date(2021, 1, 1)),
            "s2": (date(2022, 1, 1), date(2023, 1, 1))
        }
        rc = RunConfig(expectedConfig)
        # Act
        assertedConfig = rc.stocks

        # Assert
        self.assertEqual(2, len(assertedConfig))

        assertedPeriodS1 = assertedConfig["s1"]
        self.assertEqual(date(2020, 1, 1), assertedPeriodS1[0])
        self.assertEqual(date(2021, 1, 1), assertedPeriodS1[1])

        assertedPeriodS2 = assertedConfig["s2"]
        self.assertEqual(date(2022, 1, 1), assertedPeriodS2[0])
        self.assertEqual(date(2023, 1, 1), assertedPeriodS2[1])

    def test_WHEN_check_that_from_LT_untill_THEN_error(self):
        # Array
        # Array
        expectedConfig = {
            "s1": (date(2021, 1, 1), date(2021, 1, 1)),
            "s2": (date(2022, 1, 1), date(2023, 1, 1))
        }
        # Act

        # Assert
        with self.assertRaises(AttributeError) as context:
            rc = RunConfig(expectedConfig)

    def test_WHEN_config_is_imutable_THEN_nothing_can_be_changed(self):
        # Array
        expectedConfig = {
            "s1": (date(2020, 1, 1), date(2021, 1, 1)),
            "s2": (date(2022, 1, 1), date(2023, 1, 1))
        }
        rc = RunConfig(expectedConfig)

        # Act1
        config = rc.stocks
        config["s9"] = (date(2022, 1, 1), date(2023, 1, 1))

        # Act2
        config = rc.stocks
        with self.assertRaises(TypeError) as context:
            config["s1"][0] = date(2020, 1, 2)

        with self.assertRaises(TypeError) as context:
            config["s1"][1] = date(2020, 1, 2)

        # Assert
        assertedConfig = rc.stocks
        self.assertEqual(2, len(assertedConfig))

        assertedPeriodS1 = assertedConfig["s1"]
        self.assertEqual(date(2020, 1, 1), assertedPeriodS1[0])
        self.assertEqual(date(2021, 1, 1), assertedPeriodS1[1])

        assertedPeriodS2 = assertedConfig["s2"]
        self.assertEqual(date(2022, 1, 1), assertedPeriodS2[0])
        self.assertEqual(date(2023, 1, 1), assertedPeriodS2[1])

    def test_WHEN_pass_parameters_THEN_they_save_correctly(self):
        # Array
        expectedParameters = {
            "p1": [2, 3, 5],
            "p2": range(3)
        }
        rc = RunConfig.buildSameTradeInterval(
            ["s1", "s2"], date(2020, 1, 1), date(2021, 1, 1), expectedParameters)

        # Act

        # Assert
        assertedParameters = rc.parameters
        self.assertEqual(2, len(assertedParameters))

        p1 = assertedParameters["p1"]
        self.assertEqual(3, len(p1))
        self.assertIn(2, p1)
        self.assertIn(3, p1)
        self.assertIn(5, p1)

        p2 = assertedParameters["p2"]
        self.assertEqual(3, len(p2))
        self.assertIn(0, p2)
        self.assertIn(1, p2)
        self.assertIn(2, p2)

    def test_WHEN_parameters_imutable_THEN_get_error(self):
        # Array
        expectedParameters = {
            "p1": [2, 3, 5],
            "p2": range(3)
        }
        rc = RunConfig.buildSameTradeInterval(
            ["s1", "s2"], date(2020, 1, 1), date(2021, 1, 1), expectedParameters)

        # Act

        rc.parameters["p3"] = [3, 5]
        rc.parameters["p1"][0] = 99

        # Assert
        assertedParameters = rc.parameters
        self.assertEqual(2, len(assertedParameters))

        p1 = assertedParameters["p1"]
        self.assertEqual(3, len(p1))
        self.assertIn(2, p1)
        self.assertIn(3, p1)
        self.assertIn(5, p1)

        p2 = assertedParameters["p2"]
        self.assertEqual(3, len(p2))
        self.assertIn(0, p2)
        self.assertIn(1, p2)
        self.assertIn(2, p2)

    def test_WHEN_request_records_THEN_get_full_list_of_combination(self):
        # Array
        expectedParameters = {
            "p1": [2, 3, 5],
            "p2": range(3)
        }
        rc = RunConfig.buildSameTradeInterval(
            ["s1", "s2"], date(2020, 1, 1), date(2021, 1, 1), expectedParameters)

        # Act
        records = rc.records

        # Assert
        self.assertEqual(9, len(records))
        self.assertIn({"p1": 2, "p2": 0}, records)
        self.assertIn({"p1": 2, "p2": 1}, records)
        self.assertIn({"p1": 2, "p2": 2}, records)

        self.assertIn({"p1": 3, "p2": 0}, records)
        self.assertIn({"p1": 3, "p2": 1}, records)
        self.assertIn({"p1": 3, "p2": 2}, records)

        self.assertIn({"p1": 5, "p2": 0}, records)
        self.assertIn({"p1": 5, "p2": 1}, records)
        self.assertIn({"p1": 5, "p2": 2}, records)

    def test_WHEN_request_records_THEN_get_only_valid_records(self):
        # Array
        expectedParameters = {
            "p1": [2, 3, 5],
            "p2": range(3)
        }
        rc = RunConfig.buildSameTradeInterval(
            ["s1", "s2"], date(2020, 1, 1), date(2021, 1, 1), expectedParameters, lambda conf: not (conf["p1"] == 3 and conf["p2"] == 2))

        # Act
        records = rc.records

        # Assert
        self.assertEqual(8, len(records))
        self.assertIn({"p1": 2, "p2": 0}, records)
        self.assertIn({"p1": 2, "p2": 1}, records)
        self.assertIn({"p1": 2, "p2": 2}, records)

        self.assertIn({"p1": 3, "p2": 0}, records)
        self.assertIn({"p1": 3, "p2": 1}, records)
        # self.assertIn({"p1": 3, "p2": 2}, records)

        self.assertIn({"p1": 5, "p2": 0}, records)
        self.assertIn({"p1": 5, "p2": 1}, records)
        self.assertIn({"p1": 5, "p2": 2}, records)
