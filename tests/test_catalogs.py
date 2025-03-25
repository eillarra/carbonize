"""Tests for the catalogs module."""

import pytest

from carbonize.catalogs import AircraftCatalog, AirportCatalog
from carbonize.type_definitions import Aircraft, Airport


class TestAircraftCatalog:
    """Tests for the Aircraft catalog."""

    @pytest.fixture(autouse=True)
    def setup_data(self):  # noqa: D102
        self.catalog = AircraftCatalog()

    def test_get(self):  # noqa: D102
        aircraft = self.catalog.get(AircraftCatalog.DEFAULT)
        assert aircraft.code == AircraftCatalog.DEFAULT
        assert isinstance(aircraft.fuel_consumption[0], int)
        assert isinstance(aircraft, Aircraft)

        with pytest.raises(ValueError):
            self.catalog.get("Wright")


class TestAirportCatalog:
    """Tests for the Airport catalog."""

    @pytest.fixture(autouse=True)
    def setup_data(self):  # noqa: D102
        self.catalog = AirportCatalog()

    def test_get(self):  # noqa: D102
        airport = self.catalog.get("BRU")
        assert airport.code == "BRU"
        assert airport.city == "Zaventem"
        assert isinstance(airport, Airport)

        with pytest.raises(ValueError):
            self.catalog.get("000")

    def test_find(self):  # noqa: D102
        assert self.catalog.find("BE").code == "ANR"
        assert self.catalog.find("BE", "Zaventem").code == "BRU"

        with pytest.raises(ValueError):
            self.catalog.find("Milliways")
