from typing import List, NamedTuple, NewType


CarbonEmissions = NewType('CarbonEmissions', float)
FuelKg = NewType('FuelKg', float)
Km = NewType('Km', int)


class Point(NamedTuple):
    latitude: float
    longitude: float


class Aircraft(NamedTuple):
    code: str
    fuel_consumption: List[int]


class Airport(NamedTuple):
    code: str
    country: str
    city: str
    latitude: float
    longitude: float

    @property
    def point(self) -> Point:
        return Point(self.latitude, self.longitude)
