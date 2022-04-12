import os
import pickle

from typing import Dict, List

from .types import Aircraft, Airport


def get_pickle(filename) -> list:
    try:
        data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
        with open(os.path.join(data_dir, filename), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:  # pragma: no cover ; we only need this for `bin/update_data.py``
        return []


class AircraftCatalog:
    DEFAULT = "320"  # AIRBUS
    DEFAULT_LONG_DISTANCE = "777"  # BOEING

    aircrafts_dict: Dict[str, Aircraft] = {aircraft.code: aircraft for aircraft in get_pickle("icao_aircrafts.pkl")}

    def get(self, aircraft_code: str) -> Aircraft:
        try:
            return self.aircrafts_dict[aircraft_code]
        except KeyError:
            raise ValueError


class AirportCatalog:
    airports: List[Airport] = get_pickle("iata_airports.pkl")
    airports_dict: Dict[str, Airport] = {airport.code: airport for airport in get_pickle("iata_airports.pkl")}

    def get(self, airport_code: str) -> Airport:
        try:
            return self.airports_dict[airport_code]
        except KeyError:
            raise ValueError

    def find(self, country_code: str, city: str = None) -> Airport:
        try:
            if city:
                return next(a for a in self.airports if a.country == country_code and a.city == city)
            return next(a for a in self.airports if a.country == country_code)
        except StopIteration:
            raise ValueError
