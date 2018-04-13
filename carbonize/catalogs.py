import bisect
import csv
import os

from typing import List

from .typing import Aircraft, Airport, FuelKg, Km


DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def open_data_csv(filename: str):
    output: List[List[str]] = []
    with open(os.path.join(DATA_DIR, filename)) as csvfile:
        r = csv.reader(csvfile)
        for row in r:
            output.append(row)
    return output


class AircraftCatalog:
    DEFAULT = '320'  # AIRBUS
    DEFAULT_LONG_DISTANCE = '787'  # BOEING

    def __init__(self, *args, **kwargs):
        consumptions = {d[0]: d[1:] for d in open_data_csv('icao_fuel_consumption.csv')}
        self.aircrafts: List[Aircraft] = []

        for code in open_data_csv('icao_aircraft_codes.csv')[1:]:
            try:
                self.aircrafts.append(Aircraft(code[0], [(int(v) if v else None) for v in consumptions[code[1]]]))
            except KeyError as e:
                continue
        self.aircrafts_dict = {aircraft.code: aircraft for aircraft in self.aircrafts}

        """ICAO fuel consumption data is given per nautical mile, so we need to transform the ranges to Km first."""
        self.consumption_ranges = [int(nmi) * 1.852 for nmi in consumptions['Code']]

    def get(self, aircraft_code: str) -> Aircraft:
        try:
            return self.aircrafts_dict[aircraft_code]
        except KeyError as e:
            raise ValueError

    def get_consumption(self, distance: Km, aircraft_code: str) -> FuelKg:
        idx = bisect.bisect_left(self.consumption_ranges, distance)
        return self.aircrafts_dict[aircraft_code].fuel_consumption[idx] / self.consumption_ranges[idx] * distance


class AirportCatalog:
    def __init__(self, *args, **kwargs):
        data = [Airport(d[0], d[1], d[2], float(d[3]), float(d[4])) for d in open_data_csv('iata_airports.csv')[1:]]
        self.airports = data
        self.airports_dict = {airport.code: airport for airport in self.airports}

    def get(self, airport_code: str) -> Airport:
        try:
            return self.airports_dict[airport_code]
        except KeyError as e:
            raise ValueError

    def find(self, country_code: str, city: str = None) -> Airport:
        try:
            if city:
                return [a for a in self.airports if a.country == country_code and a.city == city][0]
            return [a for a in self.airports if a.country == country_code][0]
        except IndexError as e:
            raise ValueError
