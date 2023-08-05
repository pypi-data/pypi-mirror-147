from dataclasses import dataclass


@dataclass
class InclusiveRange:
    """
    Inclusive range, whose lower value must be <= than the upper value.
    """

    lower: float
    upper: float

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise ValueError(self.lower, self.upper)


class RangedCounter:
    """
    Counter whose value is always within the given range.

    You set its value upon construction, and can change it via its "value" property: either way,
    it will never exceed its allowed range.
    """

    def __init__(self, inclusive_range: InclusiveRange, initial_value: float):
        self._inclusive_range = inclusive_range
        self.value = initial_value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_value: float) -> None:
        self._value = min(
            max(new_value, self._inclusive_range.lower),
            self._inclusive_range.upper,
        )
