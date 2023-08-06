# Outside Clothes

A module to help choose outside clothes based on the conditions outside.

## General Usage

A list of clothes is compared to the a list of weather forecast dictionaries. If
the clothing item is appropriate for the forecast, it returns True and is
incremented. Once all comparisons are done, then the clothing item with the
lowest value is the recommended item to wear.

> See [Example Test](https://github.com/duncanvanzyl/weather-clothing/blob/main/tests/test_example.py) for basic usage.