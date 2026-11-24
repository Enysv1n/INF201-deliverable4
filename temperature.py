"""Temperature class supporting Celsius, Fahrenheit and Kelvin."""

from __future__ import annotations


class Temperature:
    """A temperature with a value and a unit ("C", "F" or "K")."""

    VALID_UNITS = ("C", "F", "K")
    TOLERANCE = 1e-9

    def __init__(self, value: float, unit: str = "C") -> None:
        if not isinstance(unit, str) or unit.upper() not in self.VALID_UNITS:
            raise ValueError(
                f"Invalid unit {unit!r}. Must be one of {self.VALID_UNITS}."
            )

        value = float(value)
        unit = unit.upper()

        if self._kelvin_from(value, unit) < -self.TOLERANCE:
            raise ValueError(
                f"{value} {unit} is below absolute zero (0 K)."
            )

        self._value = value
        self._unit = unit

    @staticmethod
    def _kelvin_from(value: float, unit: str) -> float:
        """Convert a value in the given unit to Kelvin."""
        if unit == "C":
            return value + 273.15
        if unit == "F":
            return (value - 32) * 5 / 9 + 273.15
        return value

    @property
    def value(self) -> float:
        """The temperature value (read-only)."""
        return self._value

    @property
    def unit(self) -> str:
        """The temperature unit (read-only)."""
        return self._unit
