import pytest

from carbonize.catalogs import AircraftCatalog, AirportCatalog
from carbonize.types import Aircraft, Airport


class TestAircraftCatalog:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.catalog = AircraftCatalog()

    def test_get(self):
        aircraft = self.catalog.get(AircraftCatalog.DEFAULT)
        assert aircraft.code == AircraftCatalog.DEFAULT
        assert isinstance(aircraft.fuel_consumption[0], int)
        assert isinstance(aircraft, Aircraft)


class TestAirportCatalog:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.catalog = AirportCatalog()

    def test_get(self):
        airport = self.catalog.get("BRU")
        assert airport.code == "BRU"
        assert airport.city == "Brussels"
        assert isinstance(airport, Airport)

        with pytest.raises(ValueError):
            self.catalog.get("000")

    def test_find(self):
        assert self.catalog.find("BE").code == "ANR"
        assert self.catalog.find("BE", "Brussels").code == "BRU"

        with pytest.raises(ValueError):
            self.catalog.find("Milliways")
