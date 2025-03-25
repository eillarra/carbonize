"""Tests for the data parsers module."""

from pathlib import Path

import pytest

from carbonize.data.parsers import IATAParser, ICAOParser


@pytest.fixture
def iata_parser():
    """Return an instance of the IATAParser class."""
    parent_dir = Path(__file__).resolve().parent
    return IATAParser(filename=parent_dir / "parser_files" / "iata_airports.csv")


@pytest.fixture
def icao_parser():
    """Return an instance of the ICAOParser class."""
    parent_dir = Path(__file__).resolve().parent
    return ICAOParser(filename=parent_dir / "parser_files" / "icao_v13.pdf")


@pytest.mark.parametrize(
    "airport_code,city",
    [
        ("BCN", "Barcelona"),
        ("CDG", "Paris"),
        ("JFK", "New York"),
        ("LAX", "Los Angeles"),
    ],
)
def test_iata_parser_airports(airport_code, city, iata_parser):
    """Test the IATAParser class."""
    iata_airports = iata_parser.get_airports()
    airports_dict = {airport.code: airport.city for airport in iata_airports}
    assert city in airports_dict[airport_code]


def test_icao_parser_aircraft_codes(icao_parser):
    """Test the ICAOParser class."""
    aircraft_code_pairs = icao_parser.get_aircraft_code_pairs()
    assert ["CN2", "MU2"] in aircraft_code_pairs
    assert len(aircraft_code_pairs) == 378


def test_icao_parser_aircrafts(icao_parser):
    """Test the ICAOParser class."""
    aircraft_codes = set([codes[0] for codes in icao_parser.get_aircraft_code_pairs()])
    aircrafts = icao_parser.get_aircrafts()
    assert all([aircraft.code in aircraft_codes for aircraft in aircrafts])
