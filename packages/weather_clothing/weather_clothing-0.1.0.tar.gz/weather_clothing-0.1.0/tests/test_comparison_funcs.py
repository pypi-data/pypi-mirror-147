from weather_clothing.comparisons import (
    equal,
    greater_than,
    greater_than_equal,
    less_than,
    less_than_equal,
    not_equal,
)
import pytest


@pytest.mark.parametrize(
    "test_forecast,test_value,expected", [(1, 2, True), (2, 1, False), (1, 1, False)]
)
def test_less_than(test_forecast, test_value, expected):
    assert less_than(test_forecast, test_value) == expected


@pytest.mark.parametrize(
    "test_forecast,test_value,expected",
    [("asdf", 1, TypeError), (1, "asdf", TypeError)],
)
def test_less_than_exception(test_forecast, test_value, expected):
    with pytest.raises(expected):
        less_than(test_forecast, test_value)


@pytest.mark.parametrize(
    "test_forecast,test_value,expected", [(1, 2, True), (2, 1, False), (1, 1, True)]
)
def test_less_than_equal(test_forecast, test_value, expected):
    assert less_than_equal(test_forecast, test_value) == expected


@pytest.mark.parametrize(
    "test_forecast,test_value,expected",
    [("asdf", 1, TypeError), (1, "asdf", TypeError)],
)
def test_less_than_equal_exception(test_forecast, test_value, expected):
    with pytest.raises(expected):
        less_than_equal(test_forecast, test_value)


@pytest.mark.parametrize(
    "test_forecast,test_value,expected", [(1, 2, False), (2, 1, False), (1, 1, True)]
)
def test_equal(test_forecast, test_value, expected):
    assert equal(test_forecast, test_value) == expected


@pytest.mark.parametrize(
    "test_forecast,test_value,expected",
    [
        pytest.param("asdf", 1, TypeError, marks=pytest.mark.xfail),
        pytest.param(1, "asdf", TypeError, marks=pytest.mark.xfail),
    ],
)
def test_equal_exception(test_forecast, test_value, expected):
    # Todo: This might be a bug. Check if this can be modified.
    with pytest.raises(expected):
        less_than_equal(test_forecast, test_value)


@pytest.mark.parametrize(
    "test_forecast,test_value,expected", [(1, 2, False), (2, 1, True), (1, 1, True)]
)
def test_greater_than_equal(test_forecast, test_value, expected):
    assert greater_than_equal(test_forecast, test_value) == expected


@pytest.mark.parametrize(
    "test_forecast,test_value,expected",
    [("asdf", 1, TypeError), (1, "asdf", TypeError)],
)
def test_greater_than_equal_exception(test_forecast, test_value, expected):
    with pytest.raises(expected):
        greater_than_equal(test_forecast, test_value)


@pytest.mark.parametrize(
    "test_forecast,test_value,expected", [(1, 2, False), (2, 1, True), (1, 1, False)]
)
def test_greater_than(test_forecast, test_value, expected):
    assert greater_than(test_forecast, test_value) == expected


@pytest.mark.parametrize(
    "test_forecast,test_value,expected",
    [("asdf", 1, TypeError), (1, "asdf", TypeError)],
)
def test_greater_than_exception(test_forecast, test_value, expected):
    with pytest.raises(expected):
        greater_than(test_forecast, test_value)


@pytest.mark.parametrize(
    "test_forecast,test_value,expected", [(1, 2, True), (2, 1, True), (1, 1, False)]
)
def test_not_equal(test_forecast, test_value, expected):
    assert not_equal(test_forecast, test_value) == expected


@pytest.mark.parametrize(
    "test_forecast,test_value,expected",
    [
        pytest.param("asdf", 1, TypeError, marks=pytest.mark.xfail),
        pytest.param(1, "asdf", TypeError, marks=pytest.mark.xfail),
    ],
)
def test_not_equal_exception(test_forecast, test_value, expected):
    # Todo: This might be a bug. Check if this can be modified.
    with pytest.raises(expected):
        not_equal(test_forecast, test_value)
