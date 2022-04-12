import unittest

from carbonize.calculators import Flight
from carbonize.utils import great_circle


class TestFlight(unittest.TestCase):
    """The values should be approximate to the results we get at:
    https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx"""

    @classmethod
    def setUpClass(self):
        self._c = Flight(a="BRU", b="BCN")
        self.step = self._c.get_step()

    def test_distance(self):
        gc = great_circle(self._c.a.point, self._c.b.point)
        self.assertAlmostEqual(self.step.distance, 1185, delta=10)
        self.assertEqual(gc + 100, self.step.distance)

    def test_fuel_consumption(self):
        self.assertAlmostEqual(self.step.fuel_consumption, 5412, delta=150)

    def test_emissions_pax(self):
        self.assertAlmostEqual(self.step.co2e, 116, delta=5)
