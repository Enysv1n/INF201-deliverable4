from math import gcd


class Fraction:
    """A fraction with an integer numerator and a positive integer denominator."""

    def __init__(self, numerator, denominator=1):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("numerator and denominator must be integers")
        if denominator <= 0:
            raise ValueError("denominator must be strictly positive")

        # Reduce the fraction, e.g. 2/4 becomes 1/2
        common = gcd(numerator, denominator)
        self.numerator = numerator // common
        self.denominator = denominator // common

    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    # Comparisons: a/b < c/d is the same as a*d < c*b (since b and d are positive)
    def __eq__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __ne__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator != other.numerator * self.denominator

    def __lt__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __ge__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator >= other.numerator * self.denominator

    # Arithmetic
    def __add__(self, other):
        new_num = self.numerator * other.denominator + other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)

    def __sub__(self, other):
        new_num = self.numerator * other.denominator - other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)

    def __mul__(self, other):
        new_num = self.numerator * other.numerator
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)

    def __truediv__(self, other):
        if other.numerator == 0:
            raise ZeroDivisionError("cannot divide by zero")
        new_num = self.numerator * other.denominator
        new_den = self.denominator * other.numerator
        # Keep the denominator positive, e.g. 1/-2 becomes -1/2
        if new_den < 0:
            new_num = -new_num
            new_den = -new_den
        return Fraction(new_num, new_den)

