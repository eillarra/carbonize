"""Module for catalogs of aircrafts and airports."""

import os
import pickle
from typing import Optional

from .type_definitions import Aircraft, Airport


def get_pickle(filename: str) -> list:
    """Load a pickle file from the data directory.

    :param filename: The name of the pickle file.
    :returns: The data from the pickle file.
    """
    try:
        data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
        with open(os.path.join(data_dir, filename), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:  # pragma: no cover ; we only need this for `bin/update_data.py``
        return []


class AircraftCatalog:
    """A catalog of aircrafts."""

    DEFAULT = "320"  # AIRBUS
    DEFAULT_LONG_DISTANCE = "777"  # BOEING

    aircrafts_dict: dict[str, Aircraft] = {aircraft.code: aircraft for aircraft in get_pickle("icao_aircrafts.pkl")}

    def get(self, aircraft_code: str) -> Aircraft:
        """Get an aircraft by its ICAO code.

        :param aircraft_code: The ICAO code of the aircraft.
        :returns: The aircraft.
        :raises ValueError: If the aircraft is not found.
        """
        try:
            return self.aircrafts_dict[aircraft_code]
        except KeyError as exc:
            raise ValueError from exc


class AirportCatalog:
    """A catalog of airports."""

    airports: list[Airport] = get_pickle("iata_airports.pkl")
    airports_dict: dict[str, Airport] = {airport.code: airport for airport in get_pickle("iata_airports.pkl")}

    def get(self, airport_code: str) -> Airport:
        """Get an airport by its IATA code.

        :param airport_code: The IATA code of the airport.
        :returns: The airport.
        :raises ValueError: If the airport is not found.
        """
        try:
            return self.airports_dict[airport_code]
        except KeyError as exc:
            raise ValueError from exc

    def find(self, country_code: str, city: Optional[str] = None) -> Airport:
        """Find an airport by its country and city.

        :param country_code: The country code of the airport.
        :param city: The city of the airport.
        :returns: The airport.
        :raises ValueError: If the airport is not found.
        """
        try:
            if city:
                return next(a for a in self.airports if a.country == country_code and a.city == city)
            return next(a for a in self.airports if a.country == country_code)
        except StopIteration as exc:
            raise ValueError from exc
