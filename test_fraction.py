import pytest

from fraction import Fraction


# Initialisation
def test_init():
    f = Fraction(3, 4)
    assert f.numerator == 3
    assert f.denominator == 4


def test_default_denominator():
    f = Fraction(5)
    assert f.denominator == 1


def test_fraction_is_reduced():
    f = Fraction(2, 4)
    assert f.numerator == 1
    assert f.denominator == 2


# Validation
@pytest.mark.parametrize("den", [0, -3])
def test_denominator_must_be_positive(den):
    with pytest.raises(ValueError):
        Fraction(1, den)


@pytest.mark.parametrize("num, den", [(1.5, 2), (1, 2.0), ("1", 2)])
def test_must_be_integers(num, den):
    with pytest.raises(TypeError):
        Fraction(num, den)


# Comparisons
def test_equal():
    assert Fraction(1, 2) == Fraction(2, 4)


def test_not_equal():
    assert Fraction(1, 2) != Fraction(1, 3)


def test_less_than():
    assert Fraction(1, 3) < Fraction(1, 2)
    assert not Fraction(1, 2) < Fraction(1, 3)


def test_less_than_or_equal():
    assert Fraction(1, 3) <= Fraction(1, 2)
    assert Fraction(1, 2) <= Fraction(2, 4)


def test_greater_than():
    assert Fraction(3, 4) > Fraction(1, 2)
    assert not Fraction(1, 2) > Fraction(3, 4)


def test_greater_than_or_equal():
    assert Fraction(3, 4) >= Fraction(1, 2)
    assert Fraction(1, 2) >= Fraction(2, 4)


def test_negative_fractions():
    assert Fraction(-1, 2) < Fraction(1, 4)


def test_compare_with_non_fraction():
    assert Fraction(1, 2).__eq__(0.5) is NotImplemented
    with pytest.raises(TypeError):
        Fraction(1, 2) < 1


# Arithmetic
def test_add():
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)


def test_sub():
    assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)


def test_mul():
    assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)


def test_div():
    assert Fraction(1, 2) / Fraction(1, 4) == Fraction(2)


def test_div_by_negative_keeps_denominator_positive():
    result = Fraction(1, 2) / Fraction(-1, 3)
    assert result == Fraction(-3, 2)
    assert result.denominator > 0


def test_div_by_zero():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0)


# String representations
def test_str():
    assert str(Fraction(3, 4)) == "3/4"


def test_repr():
    assert repr(Fraction(3, 4)) == "Fraction(3, 4)"