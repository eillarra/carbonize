import unittest

from carbonize.api import Footprint


class TestFootprint(unittest.TestCase):
    """The values should be approximate to the results we get at:
    https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx"""

    @classmethod
    def setUpClass(self):
        self.fp = Footprint()

    def test_flight(self):
        self.fp = Footprint()
        self.fp.add_flight(a="BRU", b="BCN")
        self.assertEqual(len(self.fp.steps), 1)
        self.assertAlmostEqual(self.fp.emissions, 116, delta=5)

    def test_flight_two_way(self):
        self.fp = Footprint()
        self.fp.add_flight(a="BRU", b="BCN")
        self.fp.add_flight(a="BRU", b="BCN", two_way=True)
        self.assertEqual(len(self.fp.steps), 3)
        self.assertAlmostEqual(self.fp.emissions, 116 * 3, delta=10)
