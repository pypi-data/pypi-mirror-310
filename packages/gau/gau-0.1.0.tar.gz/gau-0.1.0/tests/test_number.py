import pytest
from gau.number import is_palindrome


@pytest.mark.parametrize(
    "x, expected",
    [
        (121, True),
        (12321, True),
        (12345, False),
        (0, True),
        (-121, False),
    ]
)
def test_is_palindrome(x, expected):
    assert is_palindrome(x) == expected
