import pytest
from gau.transformer import flat, json_compact_dumps, json_loads


@pytest.mark.parametrize(
    'data, expected',
    [
        (
            {'a': 1, 'b': {'c': 2, 'd': [3, 4]}},
            {'a': 1, 'b.c': 2, 'b.d.0': 3, 'b.d.1': 4}
        ),
        (
            [{'a': 1}, {'b': 2}],
            {'0.a': 1, '1.b': 2}
        ),
        # Add more test cases here
    ]
)
def test_flat(data, expected):
    assert flat(data) == expected


@pytest.mark.parametrize(
    "params, sort_keys, expected",
    [
        ({'a': 1, 'b': 2}, True, '{"a":1,"b":2}'),
        ([1, 2, 3], False, '[1,2,3]'),
        ("hello", True, '"hello"')
    ]
)
def test_json_compact_dumps(params, sort_keys, expected):
    assert json_compact_dumps(params, sort_keys) == expected


@pytest.mark.parametrize(
    "json_str, expected",
    [
        ('{"a":1,"b":2}', {'a': 1, 'b': 2}),
        ('[1,2,3]', [1, 2, 3]),
        ('"hello"', "hello")
    ]
)
def test_json_loads(json_str, expected):
    assert json_loads(json_str) == expected
