from dataclasses import dataclass, field
from typing import Optional, Union

from .comparisons import Comparison


@dataclass
class ClothingItem:
    """An object representing an item of clothing.

    Args:
        name (str): The name of the clothing item.
        priority (int): The priority of the clothing item. Lower values should
            be given precidence.
        criteria (list[Comparison]): A list of criteria to test against a
            weather forecast dictionary.
        min_count (int): The minimum number of times this item must meet all the
            criteria. Default = 2.

    """

    name: str
    priority: int
    criteria: list[Comparison]
    min_count: int = 2
    _count: int = field(repr=False, default=0)

    def meets_criteria(self, forecast: dict[str, Union[float, str]]) -> bool:
        """Tests the comparisons against the provided forecast. If all of the
        comparisons meet the criteria, then returns True.

        Args:
            forecast (dict[str, float  |  str]): A forcast dictionary.

        Returns:
            bool: True if all comparisons are True.
        """
        for comparison in self.criteria:
            if not comparison.compare(forecast):
                return False
        return True

    @property
    def value(self) -> Optional[int]:
        """Returns its priority if the it has met the required criteria at least
        min_count times.

        Returns:
            int | None: The clothing item's priority if it has been incremented
                        at least min_count times.
        """
        return None if self._count < self.min_count else self.priority

    def inc(self):
        """Increment the clothing item counter."""
        self._count += 1
