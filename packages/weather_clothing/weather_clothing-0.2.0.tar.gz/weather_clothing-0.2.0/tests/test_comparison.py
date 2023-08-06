import pytest

from weather_clothing.comparisons import Comparison, less_than


@pytest.mark.parametrize(
    "test_forecast,test_value,expected", [(4, 5, True), (6, 5, False)]
)
def test_comparison(test_forecast, test_value, expected):
    c = Comparison("temperature", less_than, test_value)
    assert c.compare({"temperature": test_forecast}) == expected


@pytest.mark.parametrize(
    "test_key,test_value,expected",
    [("temperature", "asdf", TypeError), ("asdf", 5, KeyError)],
)
def test_comparison_exception(test_key, test_value, expected):
    c = Comparison("temperature", less_than, 5)
    with pytest.raises(expected):
        c.compare({test_key: test_value})
