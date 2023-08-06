from typing import Any

from weather_clothing.clothing_item import ClothingItem
from weather_clothing.comparisons import operator_map as om

from example_config import (
    example_boots_config,
    example_jacket_config,
    example_pants_config,
)
from example_forecast import example_forecast as forecast


def clothing_from_config(config: dict[str, Any]) -> list[ClothingItem]:
    clothing_items: list[ClothingItem] = []
    count: int = 0
    for jacket in config:
        comparisons = [
            om.comparison_from_string(comparison) for comparison in config[jacket]
        ]
        clothing_items.append(ClothingItem(jacket, count, comparisons))
        count += 1
    return clothing_items


def test_example():
    jackets = clothing_from_config(example_jacket_config)
    pants = clothing_from_config(example_pants_config)
    boots = clothing_from_config(example_boots_config)

    for items in (jackets, pants, boots):
        for prediction in forecast:
            for item in items:
                if item.meets_criteria(prediction):
                    item.inc()

    for items in (jackets, pants, boots):
        for item in items:
            print(f"{item.name} = {item.value}, {item._count}")

    for items, expected in (
        (jackets, "Winter Jacket"),
        (pants, "Rain Pants"),
        (boots, "Winter Boots"),
    ):

        priority = min([item.value for item in items if item.value is not None])
        recommended = next((item for item in items if item.value == priority), None)
        if recommended is None:
            raise ValueError("no recommedation")
        print(recommended.name)
        assert recommended is not None
        assert recommended.name == expected


if __name__ == "__main__":
    test_example()
