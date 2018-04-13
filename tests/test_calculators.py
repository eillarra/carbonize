import unittest

from carbonize.calculators import AviationCalculator
from carbonize.utils import great_circle


class TestAviationCalculator(unittest.TestCase):
    """The values should be approximate to the results we get at:
    https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx"""

    @classmethod
    def setUpClass(self):
        self._calculator = AviationCalculator('BRU', 'BCN')

    def test_distance(self):
        gc = great_circle(self._calculator.a.point, self._calculator.b.point)
        distance = self._calculator.distance
        self.assertAlmostEqual(distance, 1185, delta=10)
        self.assertEqual(gc + 100, distance)

    def test_fuel_consumption(self):
        self.assertAlmostEqual(self._calculator.fuel_consumption, 5412, delta=150)

    def test_emissions_pax(self):
        self.assertAlmostEqual(self._calculator.emissions_pax, 116, delta=5)
