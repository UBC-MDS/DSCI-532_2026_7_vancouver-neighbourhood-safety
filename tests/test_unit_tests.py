"""
Unit tests for the Vancouver Neighbourhood Safety dashboard
"""

import sys
sys.path.append("src")
from utils import get_filtered_data
import pandas as pd

def test_filter_neighbourhood():
    """
    Test that filtering by a specific neighbourhood returns only rows belonging to that neighbourhood
    """
    df = pd.DataFrame({
        "NEIGHBOURHOOD": [
            "Downtown", "Kitsilano", "West End", "Downtown",
            "Mount Pleasant", "Kitsilano", "Downtown"
        ],
        "TYPE": [
            "Mischief", "Theft", "Break and Enter Residential/Other",
            "Theft from Vehicle", "Mischief", "Theft", "Robbery"
        ],
        "MONTH_NAME": [
            "January", "February", "January",
            "March", "January", "March", "January"
        ],
        "TIME_OF_DAY": [
            "Morning", "Evening/Night", "Afternoon",
            "Morning", "Evening/Night", "Morning", "Afternoon"
        ],
    })
    df = get_filtered_data(df, filter_nb=["Downtown"])
    assert len(df) == 3
    assert df["NEIGHBOURHOOD"].unique() == ["Downtown"]

def test_filter_multiple_conditions():
    """
    Test that filtering by multiple conditions returns only rows belonging to those conditions
    """
    df = pd.DataFrame({
        "NEIGHBOURHOOD": [
            "Downtown", "Kitsilano", "West End", "Downtown",
            "Mount Pleasant", "Kitsilano", "Downtown"
        ],
        "TYPE": [
            "Mischief", "Theft", "Break and Enter Residential/Other",
            "Theft from Vehicle", "Mischief", "Theft", "Robbery"
        ],
        "MONTH_NAME": [
            "January", "February", "January",
            "March", "January", "March", "January"
        ],
        "TIME_OF_DAY": [
            "Morning", "Evening/Night", "Afternoon",
            "Morning", "Evening/Night", "Morning", "Afternoon"
        ],
    })
    df = get_filtered_data(df, filter_nb=["Downtown", "Kitsilano"], filter_crime=["Mischief", "Theft"], filter_month=["January", "February"], filter_time=["Morning", "Evening/Night"])
    assert len(df) == 2
    assert set(df["NEIGHBOURHOOD"].unique() ) == {"Downtown", "Kitsilano"}
    assert set(df["TYPE"].unique()) == {"Mischief", "Theft"}
    assert set(df["MONTH_NAME"].unique()) == {"January", "February"}
    assert set(df["TIME_OF_DAY"].unique()) == {"Morning", "Evening/Night"}