import pytest
from weather_clothing.clothing_item import ClothingItem
from weather_clothing.comparisons import operator_map as om


@pytest.mark.parametrize(
    "test_name,test_priority,test_configs",
    [
        ("Jacket", 0, ["temperature < 5"]),
        ("Pants", 3, ["temperature > 15", "precipitation_probability > 20"]),
    ],
)
def test_create(test_name, test_priority, test_configs):
    comparisons = [om.comparison_from_string(config) for config in test_configs]
    ci = ClothingItem(test_name, test_priority, comparisons)

    assert ci.name == test_name
    assert ci.priority == test_priority
    assert len(ci.criteria) == len(test_configs)


@pytest.mark.parametrize(
    "test_name,test_priority,test_configs,test_min_count",
    [
        ("Jacket", 0, ["temperature < 5"], 1),
        ("Pants", 3, ["temperature > 15"], 8),
        ("Pants", 5, ["temperature > 15"], 0),
    ],
)
def test_inc_and_value(test_name, test_priority, test_configs, test_min_count):
    comparisons = [om.comparison_from_string(config) for config in test_configs]
    ci = ClothingItem(test_name, test_priority, comparisons, min_count=test_min_count)

    for _ in range(test_min_count):
        assert ci.value == None
        ci.inc()
    assert ci.value == test_priority


@pytest.mark.parametrize(
    "test_name,test_priority,test_configs,test_forecast,test_min_count",
    [
        ("Jacket", 0, ["temperature > 15"], {"temperature": 20}, 1),
        ("Pants", 3, ["temperature > 15"], {"temperature": 20}, 8),
        ("Pants", 5, ["temperature > 15"], {"temperature": 20}, 0),
    ],
)
def test_auto_inc(
    test_name, test_priority, test_configs, test_forecast, test_min_count
):
    comparisons = [om.comparison_from_string(config) for config in test_configs]
    ci = ClothingItem(test_name, test_priority, comparisons, min_count=test_min_count)

    for _ in range(test_min_count):
        assert ci.value == None
        ci.meets_criteria(test_forecast, True)
    assert ci.value == test_priority


@pytest.mark.parametrize(
    "test_configs,test_forecast,expected",
    [
        (["temperature < 5"], {"temperature": 4}, True),
        (
            ["temperature > 15", "precipitation_probability > 20"],
            {"temperature": 20, "precipitation_probability": 30},
            True,
        ),
        (
            ["temperature > 15", "precipitation_probability > 20"],
            {"temperature": 10, "precipitation_probability": 30},
            False,
        ),
        (
            ["temperature > 15", "precipitation_probability > 20"],
            {"temperature": 20, "precipitation_probability": 10},
            False,
        ),
    ],
)
def test_meets_criteria(test_configs, test_forecast, expected):
    test_name = "Test"
    test_priority = 0
    comparisons = [om.comparison_from_string(config) for config in test_configs]
    ci = ClothingItem(test_name, test_priority, comparisons)

    assert ci.meets_criteria(test_forecast) == expected


@pytest.mark.parametrize(
    "test_configs,test_forecast,expected_confidence,expected_n",
    [
        (
            ["temperature > 15", "precipitation_probability > 20"],
            [
                {"temperature": 20, "precipitation_probability": 30},
                {"temperature": 20, "precipitation_probability": 30},
            ],
            1,
            2,
        ),
        (
            ["temperature > 15", "precipitation_probability > 20"],
            [
                {"temperature": 10, "precipitation_probability": 30},
                {"temperature": 20, "precipitation_probability": 30},
            ],
            0.5,
            2,
        ),
        (
            ["temperature > 15", "precipitation_probability > 20"],
            [
                {"temperature": 20, "precipitation_probability": 10},
                {"temperature": 20, "precipitation_probability": 10},
            ],
            0,
            2,
        ),
    ],
)
def test_confidence_and_n(test_configs, test_forecast, expected_confidence, expected_n):
    test_name = "Test"
    test_priority = 0
    comparisons = [om.comparison_from_string(config) for config in test_configs]
    ci = ClothingItem(test_name, test_priority, comparisons)

    for prediction in test_forecast:
        ci.meets_criteria(prediction, True)

    assert ci.n == expected_n
    assert ci.confidence == expected_confidence
