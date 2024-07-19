import pandas as pd
import numpy as np
from child_vac_code.utilities import processing


def test_check_for_sort_on():
    """Tests the check_for_sort_on function.
    """

    expected_rows = ["LA_code", "LA_name", "LA_parent_code"]
    expected_cols_to_remove = ["LA_parent_code"]

    actual_rows, actual_cols_to_remove = processing.check_for_sort_on(
        sort_on=["LA_parent_code", "LA_name"],
        rows=["LA_code", "LA_name"],
    )

    assert actual_rows == expected_rows
    assert actual_cols_to_remove == expected_cols_to_remove


def test_sort_for_output_defined():
    """
    Tests the sort for output_defined function when there is one column to
    sort by.
    """
    input_df = pd.DataFrame(
        {
            "AgeGroup": ["<45", "45-49", "50-52", "53-54", "55-59", "60-64", "65-69",
                         "70", "71-74", "50-74", "65-70", "53<71"],
            "A": [200, 100, 200, 50, 100, 500, 300, 200, 150, 2350, 500, 1150],
            "B": [450, 500, 300, 100, 50, 250, 600, 100, 60, 1460, 700, 1100],
        }
    )

    expected = pd.DataFrame(
        {
            "AgeGroup": ["50-74", "65-70", "53<71", "45-49", "50-52", "53-54",
                         "55-59", "60-64", "65-69", "70", "71-74"],
            "A": [2350, 500, 1150, 100, 200, 50, 100, 500, 300, 200, 150],
            "B": [1460, 700, 1100, 500, 300, 100, 50, 250, 600, 100, 60],
        }
    )

    actual = processing.sort_for_output_defined(
        input_df,
        rows=["AgeGroup"],
        sort_info={"AgeGroup": ["50-74", "65-70", "53<71", "45-49", "50-52",
                                "53-54", "55-59", "60-64", "65-69", "70", "71-74"]},
    )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_sort_for_output_defined_multi_row():
    """
    Tests the sort for output_defined function when there are multiple rows,
    which sorts a dataframe by the order required for Excel tables.
    """
    input_df = pd.DataFrame(
        {
            "AgeGroup": ["<45", "<45", "70+", "70+", "50-65", "50-65", "50-65"],
            "ColDef": ["Positive", "Negative", "Inadequate", "Negative", "Negative",
                       "Inadequate", "Positive"],
            "A": [100, 200, 50, 900, 450, 900, 1000],
            "B": [200, 100, 20, 400, 800, 100, 30],
        }
    )

    expected = pd.DataFrame(
        {
            "AgeGroup": ["<45", "<45", "50-65", "50-65", "50-65", "70+", "70+"],
            "ColDef": ["Positive", "Negative", "Positive", "Negative", "Inadequate",
                       "Negative", "Inadequate"],
            "A": [100, 200, 1000, 450, 900, 900, 50],
            "B": [200, 100, 30, 800, 100, 400, 20],
        }
    )

    actual = processing.sort_for_output_defined(
        input_df,
        rows=["AgeGroup", "ColDef"],
        sort_info={"AgeGroup": ["<45", "50-65", "70+"],
                   "ColDef": ["Positive", "Negative", "Inadequate"]},
    )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_sort_for_output():
    """
    Tests the sort for output function
    """

    input_df = pd.DataFrame(
        {
            "Org_Name": ["Bolton", "Bradford", "Camden", "Cumbria", "Gateshead",
                         "Hartlepool", "Islington", "Leeds", "Liverpool",
                         "Rotherham", "Tameside", "Westminster"],
            "Parent_OrgONSCode": ["E12000002", "E12000003", "E12000007",
                                  "E12000001", "E12000001", "E12000001",
                                  "E12000007", "E12000003", "E12000002",
                                  "E12000003", "E12000002", "E12000007"],
            "A": [150, 300, 500, 800, 50, 100, 700, 350, 960, 10, 200, 750],
        }
    )

    expected = pd.DataFrame(
        {
            "Org_Name": ["Cumbria", "Gateshead", "Hartlepool", "Bolton",
                         "Liverpool", "Tameside", "Bradford", "Leeds",
                         "Rotherham", "Camden", "Islington", "Westminster"],
            "A": [800, 50, 100, 150, 960, 200, 300, 350, 10, 500, 700, 750],
        }
    )

    actual = processing.sort_for_output(
        input_df,
        sort_on=["Parent_OrgONSCode", "Org_Name"],
        cols_to_remove=['Parent_OrgONSCode'],
    )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_apply_hepb_suppression():
    """
    Tests the apply_suppression function, using various examples of row combinations

    """
    test_input = pd.DataFrame({"Population": [0, 1, 2, 8, 8, 8],
                               "Vaccinated": [0, 1, 1, 0, 1, 5],
                               "Coverage":   [0, 100.0, 50.0, 0, 12.5, 62.5]})

    actual = processing.apply_hepb_suppression(test_input, "Population",
                                               "Vaccinated", "Coverage")

    expected = pd.DataFrame({"Population": [0, "*", "*", 8,   8,   8],
                             "Vaccinated": [0, "*", "*", "*", "*", 5],
                             "Coverage":   [0, "*", "*", "*", "*", 62.5]})

    pd.testing.assert_frame_equal(actual, expected, check_dtype=False)
