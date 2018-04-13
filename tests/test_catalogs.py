import unittest

from carbonize.catalogs import AircraftCatalog, AirportCatalog
from carbonize.typing import Aircraft, Airport


class TestAircraftCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._catalog = AircraftCatalog()

    def test_data(self):
        self.assertEqual(len(self._catalog.consumption_ranges), 20)

    def test_get(self):
        aircraft = self._catalog.get(AircraftCatalog.DEFAULT)
        self.assertEqual(aircraft.code, AircraftCatalog.DEFAULT)
        self.assertIsInstance(aircraft.fuel_consumption[0], int)
        self.assertIsInstance(aircraft, Aircraft)

    def test_get_consumption(self):
        idx = 3
        aircraft = self._catalog.get(AircraftCatalog.DEFAULT)
        consumption = self._catalog.get_consumption(self._catalog.consumption_ranges[idx], AircraftCatalog.DEFAULT)
        self.assertAlmostEqual(consumption, aircraft.fuel_consumption[idx])


class TestAirportCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._catalog = AirportCatalog()

    def test_get(self):
        airport = self._catalog.get('BRU')
        self.assertEqual(airport.code, 'BRU')
        self.assertEqual(airport.city, 'Brussels')
        self.assertIsInstance(airport, Airport)

        with self.assertRaises(ValueError):
            self._catalog.get('000')

    def test_find(self):
        self.assertEqual(self._catalog.find('BE').code, 'ANR')
        self.assertEqual(self._catalog.find('BE', 'Brussels').code, 'BRU')

        with self.assertRaises(ValueError):
            self._catalog.find('Milliways')
