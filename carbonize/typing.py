from typing import List, NamedTuple, NewType


CarbonKg = NewType('CarbonKg', float)
FuelKg = NewType('FuelKg', float)
Km = NewType('Km', int)


class Point(NamedTuple):
    latitude: float
    longitude: float


class Aircraft(NamedTuple):
    code: str
    fuel_consumption: List[int]
    y_seats: int = 175  # AIRBUS 320 approx.


class Airport(NamedTuple):
    code: str
    country: str
    city: str
    latitude: float
    longitude: float

    @property
    def point(self) -> Point:
        return Point(self.latitude, self.longitude)


class Route(NamedTuple):
    code: int
    name: str
    pax_load_factor: float
    pax_to_freight_factor: float
