import os
import pickle

from typing import List

from .types import Aircraft, Airport


DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


class AircraftCatalog:
    DEFAULT = "320"  # AIRBUS
    DEFAULT_LONG_DISTANCE = "777"  # BOEING

    def __init__(self):
        try:
            with open(os.path.join(DATA_DIR, "icao_aircrafts.pkl"), "rb") as file:
                aircrafts = pickle.load(file)
        except FileNotFoundError:
            pass

        self.aircrafts_dict = {aircraft.code: aircraft for aircraft in aircrafts}

    def get(self, aircraft_code: str) -> Aircraft:
        try:
            return self.aircrafts_dict[aircraft_code]
        except KeyError:
            raise ValueError


class AirportCatalog:
    airports: List[Airport] = []

    def __init__(self):
        try:
            with open(os.path.join(DATA_DIR, "iata_airports.pkl"), "rb") as file:
                self.airports = pickle.load(file)
        except FileNotFoundError:
            pass

        self.airports_dict = {airport.code: airport for airport in self.airports}

    def get(self, airport_code: str) -> Airport:
        try:
            return self.airports_dict[airport_code]
        except KeyError:
            raise ValueError

    def find(self, country_code: str, city: str = None) -> Airport:
        try:
            if city:
                return [a for a in self.airports if a.country == country_code and a.city == city][0]
            return [a for a in self.airports if a.country == country_code][0]
        except IndexError:
            raise ValueError
