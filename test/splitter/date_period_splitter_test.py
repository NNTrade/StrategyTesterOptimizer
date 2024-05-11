import unittest
import logging
from src.splitter.date_period_splitter import DatePeriod,DatePeriodSplitter,timedelta,List
from datetime import date

class DatePeriodSplitter_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                                datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_split_2_round_splitt_THEN_split_correct_by_proportions(self):
        # Array
        using_dp = DatePeriod(date(2020,1,1), date(2020,6,29))
        assert using_dp.period_in_days == 180, f"{using_dp.period_in_days} != 180"
        
        proportions:List[timedelta|int] = [timedelta(30),timedelta(6)]
        expected_arr = [
            [DatePeriod(date(2020,1,1), date(2020,1,31)),DatePeriod(date(2020,1,31), date(2020,2,6))],
            [DatePeriod(date(2020,2,6), date(2020,3,7)),DatePeriod(date(2020,3,7), date(2020,3,13))],
            [DatePeriod(date(2020,3,13), date(2020,4,12)),DatePeriod(date(2020,4,12), date(2020,4,18))],
            [DatePeriod(date(2020,4,18), date(2020,5,18)),DatePeriod(date(2020,5,18), date(2020,5,24))],
            [DatePeriod(date(2020,5,24), date(2020,6,23)),DatePeriod(date(2020,6,23), date(2020,6,29))]
        ]
        for expect_el in expected_arr:
            assert expect_el[0].untill_date == expect_el[1].from_date, f"{expect_el[0]} and {expect_el[1]}: not connected"
            assert expect_el[0].period_in_days == 30 ,f"{expect_el[0]}: {expect_el[0].period_in_days} != 30"
            assert expect_el[1].period_in_days == 6 ,f"{expect_el[1]}: {expect_el[1].period_in_days} != 6"

        # Act
        asserted_arr = DatePeriodSplitter.split_date_period(using_dp, proportions)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr), "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(len(asserted_arr[i]), 2, "Wrong count of sub periods")
            self.assertIsInstance(asserted_arr[i][0], DatePeriod, "Wrong type of return sub period")
            self.assertIsInstance(asserted_arr[i][1], DatePeriod, "Wrong type of return sub period")
            self.assertEqual(asserted_arr[i][0], expected_arr[i][0], "Sub period is not correct")
            self.assertEqual(asserted_arr[i][1], expected_arr[i][1], "Sub period is not correct")

    def test_WHEN_split_3_round_splitt_THEN_split_correct_by_proportions(self):
        # Array
        using_dp = DatePeriod(date(2020,1,1), date(2020,6,29))
        assert using_dp.period_in_days == 180, f"{using_dp.period_in_days} != 180"
        
        proportions:List[timedelta|int] = [25,5,6]
        expected_arr = [
            [DatePeriod(date(2020,1,1), date(2020,1,26)),DatePeriod(date(2020,1,26), date(2020,1,31)),DatePeriod(date(2020,1,31), date(2020,2,6))],
            [DatePeriod(date(2020,2,6), date(2020,3,2)),DatePeriod(date(2020,3,2), date(2020,3,7)),DatePeriod(date(2020,3,7), date(2020,3,13))],
            [DatePeriod(date(2020,3,13), date(2020,4,7)),DatePeriod(date(2020,4,7), date(2020,4,12)),DatePeriod(date(2020,4,12), date(2020,4,18))],
            [DatePeriod(date(2020,4,18), date(2020,5,13)),DatePeriod(date(2020,5,13), date(2020,5,18)),DatePeriod(date(2020,5,18), date(2020,5,24))],
            [DatePeriod(date(2020,5,24), date(2020,6,18)),DatePeriod(date(2020,6,18), date(2020,6,23)),DatePeriod(date(2020,6,23), date(2020,6,29))]
        ]
        for expect_el in expected_arr:
            assert expect_el[0].untill_date == expect_el[1].from_date, f"{expect_el[0]} and {expect_el[1]}: not connected"
            assert expect_el[1].untill_date == expect_el[2].from_date, f"{expect_el[1]} and {expect_el[2]}: not connected"
            assert expect_el[0].period_in_days == 25 ,f"{expect_el[0]}: {expect_el[0].period_in_days} != 25"
            assert expect_el[1].period_in_days == 5 ,f"{expect_el[1]}: {expect_el[1].period_in_days} != 5"
            assert expect_el[2].period_in_days == 6 ,f"{expect_el[2]}: {expect_el[2].period_in_days} != 6"


        # Act
        asserted_arr = DatePeriodSplitter.split_date_period(using_dp, proportions)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr), "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(len(asserted_arr[i]), 3, "Wrong count of sub periods")
            self.assertIsInstance(asserted_arr[i][0], DatePeriod, "Wrong type of return sub period idx 0")
            self.assertIsInstance(asserted_arr[i][1], DatePeriod, "Wrong type of return sub period idx 1")
            self.assertIsInstance(asserted_arr[i][2], DatePeriod, "Wrong type of return sub period idx 2")
            self.assertEqual(asserted_arr[i][0], expected_arr[i][0], "Sub period idx 0 is not correct")
            self.assertEqual(asserted_arr[i][1], expected_arr[i][1], "Sub period idx 1 is not correct")
            self.assertEqual(asserted_arr[i][2], expected_arr[i][2], "Sub period idx 2 is not correct")

    def test_WHEN_split_not_round_splitt_and_allow_cut_tail_THEN_cut_tail(self):
        # Array
        using_dp = DatePeriod(date(2020,1,1), date(2020,7,5))
        assert using_dp.period_in_days == 186, f"{using_dp.period_in_days} != 186"
        
        proportions:List[timedelta|int] = [25,5,6]
        expected_arr = [
            [DatePeriod(date(2020,1,1), date(2020,1,26)),DatePeriod(date(2020,1,26), date(2020,1,31)),DatePeriod(date(2020,1,31), date(2020,2,6))],
            [DatePeriod(date(2020,2,6), date(2020,3,2)),DatePeriod(date(2020,3,2), date(2020,3,7)),DatePeriod(date(2020,3,7), date(2020,3,13))],
            [DatePeriod(date(2020,3,13), date(2020,4,7)),DatePeriod(date(2020,4,7), date(2020,4,12)),DatePeriod(date(2020,4,12), date(2020,4,18))],
            [DatePeriod(date(2020,4,18), date(2020,5,13)),DatePeriod(date(2020,5,13), date(2020,5,18)),DatePeriod(date(2020,5,18), date(2020,5,24))],
            [DatePeriod(date(2020,5,24), date(2020,6,18)),DatePeriod(date(2020,6,18), date(2020,6,23)),DatePeriod(date(2020,6,23), date(2020,6,29))]
        ]
        for expect_el in expected_arr:
            assert expect_el[0].untill_date == expect_el[1].from_date, f"{expect_el[0]} and {expect_el[1]}: not connected"
            assert expect_el[1].untill_date == expect_el[2].from_date, f"{expect_el[1]} and {expect_el[2]}: not connected"
            assert expect_el[0].period_in_days == 25 ,f"{expect_el[0]}: {expect_el[0].period_in_days} != 25"
            assert expect_el[1].period_in_days == 5 ,f"{expect_el[1]}: {expect_el[1].period_in_days} != 5"
            assert expect_el[2].period_in_days == 6 ,f"{expect_el[2]}: {expect_el[2].period_in_days} != 6"


        # Act
        asserted_arr = DatePeriodSplitter.split_date_period(using_dp, proportions,cut_tail=True)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr), "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(len(asserted_arr[i]), 3, "Wrong count of sub periods")
            self.assertIsInstance(asserted_arr[i][0], DatePeriod, "Wrong type of return sub period idx 0")
            self.assertIsInstance(asserted_arr[i][1], DatePeriod, "Wrong type of return sub period idx 1")
            self.assertIsInstance(asserted_arr[i][2], DatePeriod, "Wrong type of return sub period idx 2")
            self.assertEqual(asserted_arr[i][0], expected_arr[i][0], "Sub period idx 0 is not correct")
            self.assertEqual(asserted_arr[i][1], expected_arr[i][1], "Sub period idx 1 is not correct")
            self.assertEqual(asserted_arr[i][2], expected_arr[i][2], "Sub period idx 2 is not correct")

    def test_WHEN_split_not_round_splitt_and_NOT_allow_cut_tail_THEN_raise_expection(self):
        # Array
        using_dp = DatePeriod(date(2020,1,1), date(2020,7,5))
        assert using_dp.period_in_days == 186, f"{using_dp.period_in_days} != 186"
        
        proportions:List[timedelta|int] = [25,5,6]
        # Act

        # Assert
        with self.assertRaises(AttributeError):
            DatePeriodSplitter.split_date_period(using_dp, proportions,cut_tail=False)
    
    def test_WHEN_split_with_shift_config_THEN_cut_tail(self):
        #not_round_splitt_and_allow_cut_tail

        # Array
        using_dp = DatePeriod(date(2020,1,1), date(2020,3,19))
        assert using_dp.period_in_days == 78, f"{using_dp.period_in_days} != 78"
        
        proportions:List[timedelta|int] = [25,5,6]
        shift = 10
        expected_arr = [
            [DatePeriod(date(2020,1,1), date(2020,1,26)),DatePeriod(date(2020,1,26), date(2020,1,31)),DatePeriod(date(2020,1,31), date(2020,2,6))],
            [DatePeriod(date(2020,1,11), date(2020,2,5)),DatePeriod(date(2020,2,5), date(2020,2,10)),DatePeriod(date(2020,2,10), date(2020,2,16))],
            [DatePeriod(date(2020,1,21), date(2020,2,15)),DatePeriod(date(2020,2,15), date(2020,2,20)),DatePeriod(date(2020,2,20), date(2020,2,26))],
            [DatePeriod(date(2020,1,31), date(2020,2,25)),DatePeriod(date(2020,2,25), date(2020,3,1)),DatePeriod(date(2020,3,1), date(2020,3,7))],
            [DatePeriod(date(2020,2,10), date(2020,3,6)),DatePeriod(date(2020,3,6), date(2020,3,11)),DatePeriod(date(2020,3,11), date(2020,3,17))],
        ]
        for idx in range(len(expected_arr)):
            expect_el = expected_arr[idx]
            if idx > 0:
                assert expect_el[2].untill_date - expected_arr[idx-1][2].untill_date == timedelta(shift), f"idx {idx}: shift incorrect {expect_el[2].untill_date - expected_arr[idx-1][2].untill_date}"
            assert expect_el[0].untill_date == expect_el[1].from_date, f"{expect_el[0]} and {expect_el[1]}: not connected"
            assert expect_el[1].untill_date == expect_el[2].from_date, f"{expect_el[1]} and {expect_el[2]}: not connected"
            assert expect_el[0].period_in_days == 25 ,f"{expect_el[0]}: {expect_el[0].period_in_days} != 25"
            assert expect_el[1].period_in_days == 5 ,f"{expect_el[1]}: {expect_el[1].period_in_days} != 5"
            assert expect_el[2].period_in_days == 6 ,f"{expect_el[2]}: {expect_el[2].period_in_days} != 6"


        # Act
        asserted_arr = DatePeriodSplitter.split_date_period(using_dp, proportions,shift=shift,cut_tail=True)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr), "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(len(asserted_arr[i]), 3, "Wrong count of sub periods")
            self.assertIsInstance(asserted_arr[i][0], DatePeriod, "Wrong type of return sub period idx 0")
            self.assertIsInstance(asserted_arr[i][1], DatePeriod, "Wrong type of return sub period idx 1")
            self.assertIsInstance(asserted_arr[i][2], DatePeriod, "Wrong type of return sub period idx 2")
            self.assertEqual(asserted_arr[i][0], expected_arr[i][0], "Sub period idx 0 is not correct")
            self.assertEqual(asserted_arr[i][1], expected_arr[i][1], "Sub period idx 1 is not correct")
            self.assertEqual(asserted_arr[i][2], expected_arr[i][2], "Sub period idx 2 is not correct")