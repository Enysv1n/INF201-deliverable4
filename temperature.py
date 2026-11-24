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

    def to_celsius(self) -> float:
        """Return the temperature in Celsius."""
        if self._unit == "C":
            return self._value
        if self._unit == "F":
            return (self._value - 32) * 5 / 9
        return self._value - 273.15

    def to_fahrenheit(self) -> float:
        """Return the temperature in Fahrenheit."""
        if self._unit == "F":
            return self._value
        if self._unit == "C":
            return self._value * 9 / 5 + 32
        return (self._value - 273.15) * 9 / 5 + 32

    def to_kelvin(self) -> float:
        """Return the temperature in Kelvin."""
        return self._kelvin_from(self._value, self._unit)

    def convert_to(self, target_unit: str) -> Temperature:
        """Return a new Temperature converted to target_unit."""
        if (
            not isinstance(target_unit, str)
            or target_unit.upper() not in self.VALID_UNITS
        ):
            raise ValueError(
                f"Invalid unit {target_unit!r}. Must be one of {self.VALID_UNITS}."
            )

        target_unit = target_unit.upper()
        converters = {
            "C": self.to_celsius,
            "F": self.to_fahrenheit,
            "K": self.to_kelvin,
        }
        return Temperature(converters[target_unit](), target_unit)

    def __repr__(self) -> str:
        return f"Temperature({self._value!r}, {self._unit!r})"

    def __str__(self) -> str:
        symbol = "K" if self._unit == "K" else f"°{self._unit}"
        return f"{self._value:.2f} {symbol}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return abs(self.to_kelvin() - other.to_kelvin()) <= self.TOLERANCE

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self == other

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() - self.TOLERANCE

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() <= other.to_kelvin() + self.TOLERANCE

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() + self.TOLERANCE

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() >= other.to_kelvin() - self.TOLERANCE
        