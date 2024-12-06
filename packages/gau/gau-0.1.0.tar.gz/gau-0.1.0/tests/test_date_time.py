
import pytest
from datetime import datetime
from gau.date_time import prev_month


@pytest.mark.parametrize(
    "input_date, expected",
    [
        (datetime(2023, 11, 30), datetime(2023, 10, 30)),
        (datetime(2023, 3, 30), datetime(2023, 2, 28)),
        (datetime(2024, 1, 10), datetime(2023, 12, 10)),
        (datetime(2024, 3, 30), datetime(2024, 2, 29)),
    ]
)
def test_prev_month(input_date, expected):
    assert prev_month(input_date) == expected
