import unittest

from carbonize.calculators import AviationCalculator
from carbonize.utils import great_circle


class TestAviationCalculator(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._calculator = AviationCalculator()

    def test_calculate_distance(self):
        a, b = self._calculator.airports.get('BRU'), self._calculator.airports.get('BCN')
        gc = great_circle(a.point, b.point)
        distance = self._calculator.calculate_distance(a, b)
        self.assertAlmostEqual(distance, 1180, delta=10)
        self.assertEqual(gc + 100, distance)

    @unittest.skip('NotImplemented')
    def test_calculate_emissions(self):
        pass

    @unittest.skip('NotImplemented')
    def test_calculate(self):
        pass
