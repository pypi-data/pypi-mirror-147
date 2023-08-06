from weather_clothing.comparisons import (
    OperatorMap,
    equal,
    greater_than,
    less_than,
    operator_map,
)
import pytest


def test_register():
    def comparison_func(forecast: float | str, value: float | str) -> bool:
        return True

    operator = "|||"
    om = OperatorMap()

    om.register(operator, comparison_func)
    print(om._operator_map)

    assert (operator in om._operator_map) == True
    assert om._operator_map[operator] == comparison_func


@pytest.mark.parametrize(
    "test_key,test_operator,test_value,expected_comparison_func,expected_value_type",
    [
        ("temperature", "<", 5, less_than, float),
        ("temperature", "==", "asdf", equal, str),
        ("temperature", ">", "asdf", greater_than, str),
    ],
)
def test_comparison_from_string(
    test_key, test_operator, test_value, expected_comparison_func, expected_value_type
):
    config = f"{test_key} {test_operator} {test_value}"
    comparison = operator_map.comparison_from_string(config)

    assert comparison.key == test_key
    assert comparison.compare_func == expected_comparison_func
    assert comparison.value == test_value
    assert isinstance(comparison.value, expected_value_type)


@pytest.mark.parametrize(
    "test_config,expected",
    [
        ("temperature ||| 5", ValueError),
        ("temperature  5", ValueError),
        ("temperature 5", ValueError),
        ("temperature + + 5", ValueError),
    ],
)
def test_comparison_from_string_exception(test_config, expected):
    with pytest.raises(expected):
        operator_map.comparison_from_string(test_config)
