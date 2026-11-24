"""Tests for the Temperature class. Run with: pytest test_temperature.py -v"""

import pytest

from temperature import Temperature

TOL = Temperature.TOLERANCE

# Reference points as (Celsius, Fahrenheit, Kelvin)
REFERENCE_POINTS = [
    pytest.param(-273.15, -459.67, 0.0, id="absolute_zero"),
    pytest.param(-40.0, -40.0, 233.15, id="celsius_fahrenheit_crossover"),
    pytest.param(0.0, 32.0, 273.15, id="water_freezing"),
    pytest.param(37.0, 98.6, 310.15, id="human_body"),
    pytest.param(100.0, 212.0, 373.15, id="water_boiling"),
]


# ---------------------------------------------------------------------------
# 1. Initialization
# ---------------------------------------------------------------------------
def test_default_unit_is_celsius():
    t = Temperature(20)
    assert t.unit == "C"
    assert t.value == 20.0


@pytest.mark.parametrize("unit, expected", [
    ("c", "C"), ("C", "C"),
    ("f", "F"), ("F", "F"),
    ("k", "K"), ("K", "K"),
])
def test_unit_is_case_insensitive(unit, expected):
    assert Temperature(10, unit).unit == expected


def test_value_is_stored_as_float():
    assert isinstance(Temperature(25, "C").value, float)


def test_value_is_read_only():
    t = Temperature(25, "C")
    with pytest.raises(AttributeError):
        t.value = 30


def test_unit_is_read_only():
    t = Temperature(25, "C")
    with pytest.raises(AttributeError):
        t.unit = "F"


# ---------------------------------------------------------------------------
# 2. Validation
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("bad_unit", ["X", "", "Celsius", "CF", " C", None, 5])
def test_invalid_unit_raises(bad_unit):
    with pytest.raises(ValueError):
        Temperature(10, bad_unit)


@pytest.mark.parametrize("value, unit", [
    (-273.16, "C"),
    (-300, "C"),
    (-459.68, "F"),
    (-500, "F"),
    (-0.01, "K"),
    (-1, "K"),
])
def test_below_absolute_zero_raises(value, unit):
    with pytest.raises(ValueError):
        Temperature(value, unit)


@pytest.mark.parametrize("value, unit", [(-273.15, "C"), (-459.67, "F"), (0, "K")])
def test_exactly_absolute_zero_is_allowed(value, unit):
    Temperature(value, unit)  # should not raise


@pytest.mark.parametrize("bad_unit", ["X", "", "kelvin", None])
def test_convert_to_invalid_unit_raises(bad_unit):
    with pytest.raises(ValueError):
        Temperature(10, "C").convert_to(bad_unit)


# ---------------------------------------------------------------------------
# 3. Conversions
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("source_unit", ["C", "F", "K"])
@pytest.mark.parametrize("celsius, fahrenheit, kelvin", REFERENCE_POINTS)
def test_conversion_methods(celsius, fahrenheit, kelvin, source_unit):
    start = {"C": celsius, "F": fahrenheit, "K": kelvin}[source_unit]
    t = Temperature(start, source_unit)

    assert t.to_celsius() == pytest.approx(celsius, abs=TOL)
    assert t.to_fahrenheit() == pytest.approx(fahrenheit, abs=TOL)
    assert t.to_kelvin() == pytest.approx(kelvin, abs=TOL)


@pytest.mark.parametrize("target_unit", ["c", "F", "k"])
@pytest.mark.parametrize("celsius, fahrenheit, kelvin", REFERENCE_POINTS)
def test_convert_to(celsius, fahrenheit, kelvin, target_unit):
    expected = {"C": celsius, "F": fahrenheit, "K": kelvin}[target_unit.upper()]
    original = Temperature(celsius, "C")
    converted = original.convert_to(target_unit)

    assert isinstance(converted, Temperature)
    assert converted is not original
    assert converted.unit == target_unit.upper()
    assert converted.value == pytest.approx(expected, abs=TOL)


# ---------------------------------------------------------------------------
# 4. Round-trip conversions
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("celsius", [-273.15, -40.0, 0.0, 37.0, 100.0, 21.5, 1234.567])
def test_round_trip_c_f_k_c(celsius):
    original = Temperature(celsius, "C")
    result = original.convert_to("F").convert_to("K").convert_to("C")

    assert result.unit == "C"
    assert result.value == pytest.approx(original.value, abs=TOL)
    assert result == original


# ---------------------------------------------------------------------------
# 5. Cross-unit comparisons
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("celsius, fahrenheit, kelvin", REFERENCE_POINTS)
def test_equality_across_units(celsius, fahrenheit, kelvin):
    c = Temperature(celsius, "C")
    f = Temperature(fahrenheit, "F")
    k = Temperature(kelvin, "K")

    assert c == f and f == k and c == k
    assert not (c != f)
    assert c <= f and c >= f
    assert not (c < f) and not (c > f)


def test_inequality_across_units():
    assert Temperature(0, "C") != Temperature(0, "F")
    assert not (Temperature(0, "C") == Temperature(0, "F"))


def test_ordering_across_units():
    cold = Temperature(0, "C")       # 273.15 K
    warm = Temperature(80, "F")      # ~299.82 K
    hot = Temperature(400, "K")      # 400 K

    assert cold < warm < hot
    assert cold <= warm <= hot
    assert hot > warm > cold
    assert hot >= warm >= cold
    assert not (hot < cold)
    assert not (cold > hot)


def test_differences_within_tolerance_are_equal():
    a = Temperature(10, "C")
    b = Temperature(10 + TOL / 2, "C")
    assert a == b
    assert not (a < b) and not (a > b)


def test_comparison_with_non_temperature_returns_not_implemented():
    t = Temperature(25, "C")
    assert t.__eq__(25) is NotImplemented
    assert t.__lt__(25) is NotImplemented
    assert (t == 25) is False
    assert (t != 25) is True
    with pytest.raises(TypeError):
        t < 25


# ---------------------------------------------------------------------------
# 6. Formatting
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("value, unit, expected", [
    (25, "C", "25.00 °C"),
    (98.6, "f", "98.60 °F"),
    (273.15, "K", "273.15 K"),
    (-40, "F", "-40.00 °F"),
    (1 / 3, "C", "0.33 °C"),
])
def test_str(value, unit, expected):
    assert str(Temperature(value, unit)) == expected


@pytest.mark.parametrize("value, unit, expected", [
    (25, "C", "Temperature(25.0, 'C')"),
    (98.6, "f", "Temperature(98.6, 'F')"),
    (0, "k", "Temperature(0.0, 'K')"),
])
def test_repr(value, unit, expected):
    assert repr(Temperature(value, unit)) == expected


def test_repr_can_recreate_object():
    t = Temperature(37.5, "F")
    assert eval(repr(t)) == t
    