import pytest
from app.calculator import Calculator


class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_calc_correct(self):
        assert self.calc.multiply(self, 7, 8) == 56

    def test_division_calc_correct(self):
        assert self.calc.division(self, 135, 5) == 27

    def test_subtraction_calc_correct(self):
        assert self.calc.subtraction(self, 46, 48) == -2

    def test_adding_calc_correct(self):
        assert self.calc.adding(self, -3, -2) == -5
