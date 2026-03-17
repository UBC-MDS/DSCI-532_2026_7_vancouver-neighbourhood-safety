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
    df = get_filtered_data(filter_nb=["Downtown"])
    assert len(df) == 10526
    assert df["NEIGHBOURHOOD"].unique() == ["Downtown"]

def test_filter_multiple_conditions():
    """
    Test that filtering by multiple conditions returns only rows belonging to those conditions
    """
    df = get_filtered_data(filter_nb=["Downtown", "Kitsilano"], filter_crime=["Mischief"], filter_month=["January", "February"], filter_time=["Morning", "Evening/Night"])
    assert len(df) == 255
    assert set(df["NEIGHBOURHOOD"].unique() ) == {"Downtown", "Kitsilano"}
    assert set(df["TYPE"].unique()) == {"Mischief"}
    assert set(df["MONTH_NAME"].unique()) == {"January", "February"}
    assert set(df["TIME_OF_DAY"].unique()) == {"Morning", "Evening/Night"}