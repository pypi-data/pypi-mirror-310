"""
should be called timestamps.py
"""

# pylint: disable=invalid-name

# import random
import pandas as pd

SAMPLE1_raw = [

    "2021-03-12 01:00:00",
    "2022-02-11 01:00:00",
    "2023-01-10 01:00:00",
    "2024-01-01 01:00:00",
    "2024-01-01 02:00:00",
    "2024-01-01 03:00:00",
    "2024-01-02 02:00:00",
    "2024-01-02 03:00:00",
    "2024-01-03 01:00:00",
    "2024-01-03 02:00:00",
    "2024-01-03 03:00:00",
    "2024-01-10 01:00:00",
    "2024-01-10 02:00:00",
    "2024-01-10 03:00:00",
    "2024-02-01 01:00:00",
    "2024-02-01 02:00:00",
    "2024-02-01 03:00:00",
    "2024-02-02 01:00:00",
    "2024-02-02 02:00:00",
    "2024-02-02 03:00:00",
    "2024-02-03 01:00:00",
    "2024-02-03 02:00:00",
    "2024-02-03 03:00:00",
    "2024-03-01 01:00:00",
    "2024-03-01 02:00:00",
    "2024-03-01 03:00:00",
    "2024-03-02 01:00:00",
    "2024-03-02 02:00:00",
    "2024-03-02 03:00:00",
    "2024-03-03 01:00:00",
    "2024-03-03 02:00:00",
    "2024-03-03 03:00:00",
    "2024-06-01 00:00:00",
    "2024-06-01 02:00:00",
    "2024-06-01 03:00:00",
    "2024-06-01 04:00:00",
    "2024-06-01 05:00:00",
    "2024-06-01 06:00:00",
    "2024-06-01 07:00:00",
    "2024-06-01 08:00:00",
    "2024-06-01 09:00:00",
    "2024-06-01 10:00:00",
    "2024-06-01 11:00:00",
    "2024-06-01 12:00:00",
]

# shuffle the list in a reproducible way
SAMPLE1_shuffle_string = """
28 9 39 43 1
17 32 27 31 8
37 11 15 29 35
42 7 38 5 36
3 6 21 2 41
23 20 40 18 22
16 12 0 30 19
34 33 24 26 25
14 10 4 13
"""


def sample1() -> list[pd.Timestamp]:
    """
    return a list of timestamps
    """
    samples = [pd.Timestamp(x) for x in SAMPLE1_raw]
    shuffle = [int(x) for x in SAMPLE1_shuffle_string.split() if x]
    try:
        if not (0 <= i <= 44 for i in shuffle):
            raise ValueError("Invalid shuffle string")
        return [samples[i] for i in shuffle]
    except IndexError as e:
        raise ValueError("Invalid shuffle") from e


# this has 7705 entries
def sample2() -> list[pd.Timestamp]:
    """
    return all hours of 2024 between January 1st and November 17th
    """
    return list(pd.date_range('2024-01-01', '2024-11-15 23:00', freq='1h'))
