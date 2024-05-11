from typing import List
import unittest
import logging
import random as rd
from src.splitter.data_frame_plitter import DataFrameSplitter, DataFrame, Series


class DataFrameSplitter_DataFrame_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_split_to_2_sub_interval_with_round_splitt_THEN_split_correct_by_proportions(self):
        # Array
        using_A_values = [rd.random for i in range(180)]
        using_B_values = [rd.random for i in range(180)]
        using_df = DataFrame({"A": using_A_values, "B": using_B_values})
        assert len(using_df) == 180, "Dataframe len != 180"

        sub_intervals_proportions = [30, 6]
        expected_arr = [
            [using_df.iloc[0:30].copy(True), using_df.iloc[30:36].copy(True)],
            [using_df.iloc[36:66].copy(True), using_df.iloc[66:72].copy(True)],
            [using_df.iloc[72:102].copy(
                True), using_df.iloc[102:108].copy(True)],
            [using_df.iloc[108:138].copy(
                True), using_df.iloc[138:144].copy(True)],
            [using_df.iloc[144:174].copy(
                True), using_df.iloc[174:180].copy(True)],
        ]
        for idx in range(len(expected_arr)):
            expect_el = expected_arr[idx]
            assert len(expect_el[0]) == 30, f"{idx}: {len(expect_el[0])} != 30"
            assert len(expect_el[1]) == 6, f"{idx}: {len(expect_el[1])} != 6"

        # Act
        asserted_arr = DataFrameSplitter.split_data(
            using_df, sub_intervals_proportions)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr),
                         "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(
                len(asserted_arr[i]), 2, "Wrong count of sub periods")
            self.assertIsInstance(
                asserted_arr[i][0], DataFrame, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][1], DataFrame, "Wrong type of return sub period")
            asserted_df0: DataFrame = asserted_arr[i][0]  # type: ignore
            asserted_df1: DataFrame = asserted_arr[i][1]  # type: ignore

            self.assertEqual(
                len(asserted_arr[i][0].columns), 2, "Wrong column count")
            self.assertTrue(
                "A" in asserted_arr[i][0].columns, "A column doesn't exist")
            self.assertTrue(
                "B" in asserted_arr[i][0].columns, "B column doesn't exist")

            self.assertEqual(
                len(asserted_arr[i][1].columns), 2, "Wrong column count")
            self.assertTrue(
                "A" in asserted_arr[i][1].columns, "A column doesn't exist")
            self.assertTrue(
                "B" in asserted_arr[i][1].columns, "B column doesn't exist")

            self.assertTrue(asserted_df0.equals(
                expected_arr[i][0]), "Sub dataframe is not correct")
            self.assertTrue(asserted_df1.equals(
                expected_arr[i][1]), "Sub dataframe is not correct")

    def test_WHEN_split_to_3_sub_interval_with_round_splitt_THEN_split_correct_by_proportions(self):
        # Array
        using_A_values = [rd.random for i in range(180)]
        using_B_values = [rd.random for i in range(180)]
        using_df = DataFrame({"A": using_A_values, "B": using_B_values})
        assert len(using_df) == 180, "Dataframe len != 180"

        sub_intervals_proportions = [25, 5, 6]
        expected_arr = [
            [using_df.iloc[0:25].copy(True), using_df.iloc[25:30].copy(True),
             using_df.iloc[30:36].copy(True)],
            [using_df.iloc[36:61].copy(True), using_df.iloc[61:66].copy(True),
             using_df.iloc[66:72].copy(True)],
            [using_df.iloc[72:97].copy(True), using_df.iloc[97:102].copy(True),
             using_df.iloc[102:108].copy(True)],
            [using_df.iloc[108:133].copy(True), using_df.iloc[133:138].copy(True),
             using_df.iloc[138:144].copy(True)],
            [using_df.iloc[144:169].copy(True), using_df.iloc[169:174].copy(True),
             using_df.iloc[174:180].copy(True)],
        ]
        for idx in range(len(expected_arr)):
            expect_el = expected_arr[idx]
            assert len(expect_el[0]) == 25, f"{idx}: {len(expect_el[0])} != 25"
            assert len(expect_el[1]) == 5, f"{idx}: {len(expect_el[1])} != 5"
            assert len(expect_el[2]) == 6, f"{idx}: {len(expect_el[2])} != 6"

        # Act
        asserted_arr = DataFrameSplitter.split_data(
            using_df, sub_intervals_proportions)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr),
                         "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(
                len(asserted_arr[i]), 3, "Wrong count of sub periods")
            self.assertIsInstance(
                asserted_arr[i][0], DataFrame, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][1], DataFrame, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][2], DataFrame, "Wrong type of return sub period")
            asserted_df0: DataFrame = asserted_arr[i][0]  # type: ignore
            asserted_df1: DataFrame = asserted_arr[i][1]  # type: ignore
            asserted_df2: DataFrame = asserted_arr[i][2]  # type: ignore

            self.assertEqual(
                len(asserted_df0.columns), 2, "Wrong column count")
            self.assertTrue(
                "A" in asserted_df0.columns, "A column doesn't exist")
            self.assertTrue(
                "B" in asserted_df0.columns, "B column doesn't exist")

            self.assertEqual(
                len(asserted_df1.columns), 2, "Wrong column count")
            self.assertTrue(
                "A" in asserted_df1.columns, "A column doesn't exist")
            self.assertTrue(
                "B" in asserted_df1.columns, "B column doesn't exist")

            self.assertEqual(
                len(asserted_df2.columns), 2, "Wrong column count")
            self.assertTrue(
                "A" in asserted_df2.columns, "A column doesn't exist")
            self.assertTrue(
                "B" in asserted_df2.columns, "B column doesn't exist")

            self.assertTrue(asserted_df0.equals(
                expected_arr[i][0]), "Sub dataframe is not correct")
            self.assertTrue(asserted_df1.equals(
                expected_arr[i][1]), "Sub dataframe is not correct")
            self.assertTrue(asserted_df2.equals(
                expected_arr[i][2]), "Sub dataframe is not correct")

    def test_WHEN_split_to_3_sub_interval_without_round_splitt_and_allow_cut_tail_THEN_cut_tail(self):
        # Array
        using_A_values = [rd.random for i in range(186)]
        using_B_values = [rd.random for i in range(186)]
        using_df = DataFrame({"A": using_A_values, "B": using_B_values})
        assert len(using_df) == 186, "Dataframe len != 186"

        sub_intervals_proportions = [25, 5, 6]
        expected_arr = [
            [using_df.iloc[0:25].copy(True), using_df.iloc[25:30].copy(True),
             using_df.iloc[30:36].copy(True)],
            [using_df.iloc[36:61].copy(True), using_df.iloc[61:66].copy(True),
             using_df.iloc[66:72].copy(True)],
            [using_df.iloc[72:97].copy(True), using_df.iloc[97:102].copy(True),
             using_df.iloc[102:108].copy(True)],
            [using_df.iloc[108:133].copy(True), using_df.iloc[133:138].copy(True),
             using_df.iloc[138:144].copy(True)],
            [using_df.iloc[144:169].copy(True), using_df.iloc[169:174].copy(True),
             using_df.iloc[174:180].copy(True)],
        ]
        for idx in range(len(expected_arr)):
            expect_el = expected_arr[idx]
            assert len(expect_el[0]) == 25, f"{idx}: {len(expect_el[0])} != 25"
            assert len(expect_el[1]) == 5, f"{idx}: {len(expect_el[1])} != 5"
            assert len(expect_el[2]) == 6, f"{idx}: {len(expect_el[2])} != 6"

        # Act
        asserted_arr = DataFrameSplitter.split_data(
            using_df, sub_intervals_proportions, cut_tail=True)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr),
                         "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(
                len(asserted_arr[i]), 3, "Wrong count of sub periods")
            self.assertIsInstance(
                asserted_arr[i][0], DataFrame, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][1], DataFrame, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][2], DataFrame, "Wrong type of return sub period")
            asserted_df0: DataFrame = asserted_arr[i][0]  # type: ignore
            asserted_df1: DataFrame = asserted_arr[i][1]  # type: ignore
            asserted_df2: DataFrame = asserted_arr[i][2]  # type: ignore

            self.assertEqual(
                len(asserted_df0.columns), 2, "Wrong column count")
            self.assertTrue(
                "A" in asserted_df0.columns, "A column doesn't exist")
            self.assertTrue(
                "B" in asserted_df0.columns, "B column doesn't exist")

            self.assertEqual(
                len(asserted_df1.columns), 2, "Wrong column count")
            self.assertTrue(
                "A" in asserted_df1.columns, "A column doesn't exist")
            self.assertTrue(
                "B" in asserted_df1.columns, "B column doesn't exist")

            self.assertEqual(
                len(asserted_df2.columns), 2, "Wrong column count")
            self.assertTrue(
                "A" in asserted_df2.columns, "A column doesn't exist")
            self.assertTrue(
                "B" in asserted_df2.columns, "B column doesn't exist")

            self.assertTrue(asserted_df0.equals(
                expected_arr[i][0]), "Sub dataframe is not correct")
            self.assertTrue(asserted_df1.equals(
                expected_arr[i][1]), "Sub dataframe is not correct")
            self.assertTrue(asserted_df2.equals(
                expected_arr[i][2]), "Sub dataframe is not correct")

    def test_WHEN_split_to_3_sub_interval_without_round_splitt_and_NOT_allow_cut_tail_THEN_raise_expection(self):
        # Array
        using_A_values = [rd.random for i in range(186)]
        using_B_values = [rd.random for i in range(186)]
        using_df = DataFrame({"A": using_A_values, "B": using_B_values})
        assert len(using_df) == 186, "Dataframe len != 186"

        sub_intervals_proportions = [25, 5, 6]

        # Act

        # Assert
        with self.assertRaises(AttributeError):
            DataFrameSplitter.split_data(using_df, sub_intervals_proportions, cut_tail=False)


class DataFrameSplitter_Series_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_split_to_2_sub_interval_with_round_splitt_THEN_split_correct_by_proportions(self):
        # Array
        using_A_values = [rd.random for i in range(180)]
        using_sr = Series(using_A_values, name="A")
        assert len(using_sr) == 180, "Dataframe len != 180"

        sub_intervals_proportions = [30, 6]
        expected_arr = [
            [using_sr.iloc[0:30].copy(True), using_sr.iloc[30:36].copy(True)],
            [using_sr.iloc[36:66].copy(True), using_sr.iloc[66:72].copy(True)],
            [using_sr.iloc[72:102].copy(
                True), using_sr.iloc[102:108].copy(True)],
            [using_sr.iloc[108:138].copy(
                True), using_sr.iloc[138:144].copy(True)],
            [using_sr.iloc[144:174].copy(
                True), using_sr.iloc[174:180].copy(True)],
        ]
        for idx in range(len(expected_arr)):
            expect_el = expected_arr[idx]
            assert len(expect_el[0]) == 30, f"{idx}: {len(expect_el[0])} != 30"
            assert len(expect_el[1]) == 6, f"{idx}: {len(expect_el[1])} != 6"

        # Act
        asserted_arr = DataFrameSplitter.split_data(
            using_sr, sub_intervals_proportions)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr),
                         "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(
                len(asserted_arr[i]), 2, "Wrong count of sub periods")
            self.assertIsInstance(
                asserted_arr[i][0], Series, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][1], Series, "Wrong type of return sub period")
            asserted_sr0: Series = asserted_arr[i][0]  # type: ignore
            asserted_sr1: Series = asserted_arr[i][1]  # type: ignore

            self.assertEqual(asserted_sr0.name, "A",
                             "Sub Series name incorrect")
            self.assertEqual(asserted_sr1.name, "A",
                             "Sub Series name incorrect")

            self.assertTrue(asserted_sr0.equals(
                expected_arr[i][0]), "Sub series is not correct")
            self.assertTrue(asserted_sr1.equals(
                expected_arr[i][1]), "Sub series is not correct")

    def test_WHEN_split_to_3_sub_interval_with_round_splitt_THEN_split_correct_by_proportions(self):
        # Array
        using_A_values = [rd.random for i in range(180)]
        using_sr = Series(using_A_values, name="A")
        assert len(using_sr) == 180, "Dataframe len != 180"

        sub_intervals_proportions = [25, 5, 6]
        expected_arr = [
            [using_sr.iloc[0:25].copy(True), using_sr.iloc[25:30].copy(True),
             using_sr.iloc[30:36].copy(True)],
            [using_sr.iloc[36:61].copy(True), using_sr.iloc[61:66].copy(True),
             using_sr.iloc[66:72].copy(True)],
            [using_sr.iloc[72:97].copy(True), using_sr.iloc[97:102].copy(True),
             using_sr.iloc[102:108].copy(True)],
            [using_sr.iloc[108:133].copy(True), using_sr.iloc[133:138].copy(True),
             using_sr.iloc[138:144].copy(True)],
            [using_sr.iloc[144:169].copy(True), using_sr.iloc[169:174].copy(True),
             using_sr.iloc[174:180].copy(True)],
        ]
        for idx in range(len(expected_arr)):
            expect_el = expected_arr[idx]
            assert len(expect_el[0]) == 25, f"{idx}: {len(expect_el[0])} != 25"
            assert len(expect_el[1]) == 5, f"{idx}: {len(expect_el[1])} != 5"
            assert len(expect_el[2]) == 6, f"{idx}: {len(expect_el[2])} != 6"

        # Act
        asserted_arr = DataFrameSplitter.split_data(
            using_sr, sub_intervals_proportions)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr),
                         "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(
                len(asserted_arr[i]), 3, "Wrong count of sub periods")
            self.assertIsInstance(
                asserted_arr[i][0], Series, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][1], Series, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][2], Series, "Wrong type of return sub period")
            asserted_sr0: Series = asserted_arr[i][0]  # type: ignore
            asserted_sr1: Series = asserted_arr[i][1]  # type: ignore
            asserted_sr2: Series = asserted_arr[i][2]  # type: ignore

            self.assertEqual(asserted_sr0.name, "A",
                             "Sub Series name incorrect")
            self.assertEqual(asserted_sr1.name, "A",
                             "Sub Series name incorrect")
            self.assertEqual(asserted_sr2.name, "A",
                             "Sub Series name incorrect")

            self.assertTrue(asserted_sr0.equals(
                expected_arr[i][0]), "Sub series is not correct")
            self.assertTrue(asserted_sr1.equals(
                expected_arr[i][1]), "Sub series is not correct")
            self.assertTrue(asserted_sr2.equals(
                expected_arr[i][2]), "Sub series is not correct")


    def test_WHEN_split_to_3_sub_interval_without_round_splitt_and_allow_cut_tail_THEN_cut_tail(self):
        # Array
        using_A_values = [rd.random for i in range(186)]
        using_sr = Series(using_A_values, name="A")
        assert len(using_sr) == 186, "Dataframe len != 186"

        sub_intervals_proportions = [25, 5, 6]
        expected_arr = [
            [using_sr.iloc[0:25].copy(True), using_sr.iloc[25:30].copy(True),
             using_sr.iloc[30:36].copy(True)],
            [using_sr.iloc[36:61].copy(True), using_sr.iloc[61:66].copy(True),
             using_sr.iloc[66:72].copy(True)],
            [using_sr.iloc[72:97].copy(True), using_sr.iloc[97:102].copy(True),
             using_sr.iloc[102:108].copy(True)],
            [using_sr.iloc[108:133].copy(True), using_sr.iloc[133:138].copy(True),
             using_sr.iloc[138:144].copy(True)],
            [using_sr.iloc[144:169].copy(True), using_sr.iloc[169:174].copy(True),
             using_sr.iloc[174:180].copy(True)],
        ]
        for idx in range(len(expected_arr)):
            expect_el = expected_arr[idx]
            assert len(expect_el[0]) == 25, f"{idx}: {len(expect_el[0])} != 25"
            assert len(expect_el[1]) == 5, f"{idx}: {len(expect_el[1])} != 5"
            assert len(expect_el[2]) == 6, f"{idx}: {len(expect_el[2])} != 6"

        # Act
        asserted_arr = DataFrameSplitter.split_data(
            using_sr, sub_intervals_proportions,cut_tail=True)

        # Assert
        self.assertEqual(len(asserted_arr), len(expected_arr),
                         "Size of asserted sub intervals is not correct")
        for i in range(len(expected_arr)):
            self.assertEqual(
                len(asserted_arr[i]), 3, "Wrong count of sub periods")
            self.assertIsInstance(
                asserted_arr[i][0], Series, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][1], Series, "Wrong type of return sub period")
            self.assertIsInstance(
                asserted_arr[i][2], Series, "Wrong type of return sub period")
            asserted_sr0: Series = asserted_arr[i][0]  # type: ignore
            asserted_sr1: Series = asserted_arr[i][1]  # type: ignore
            asserted_sr2: Series = asserted_arr[i][2]  # type: ignore

            self.assertEqual(asserted_sr0.name, "A",
                             "Sub Series name incorrect")
            self.assertEqual(asserted_sr1.name, "A",
                             "Sub Series name incorrect")
            self.assertEqual(asserted_sr2.name, "A",
                             "Sub Series name incorrect")

            self.assertTrue(asserted_sr0.equals(
                expected_arr[i][0]), "Sub series is not correct")
            self.assertTrue(asserted_sr1.equals(
                expected_arr[i][1]), "Sub series is not correct")
            self.assertTrue(asserted_sr2.equals(
                expected_arr[i][2]), "Sub series is not correct")

    def test_WHEN_split_to_3_sub_interval_without_round_splitt_and_NOT_allow_cut_tail_THEN_raise_expection(self):
        # Array
        using_A_values = [rd.random for i in range(186)]
        using_sr = Series(using_A_values, name="A")
        assert len(using_sr) == 186, "Dataframe len != 186"

        sub_intervals_proportions = [25, 5, 6]

        # Act        

        # Assert
        with self.assertRaises(AttributeError):
            DataFrameSplitter.split_data(
            using_sr, sub_intervals_proportions,cut_tail=False)