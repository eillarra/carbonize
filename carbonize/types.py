from typing import List, NamedTuple, NewType, Optional


CarbonKg = NewType("CarbonKg", float)  # CO2e
FuelKg = NewType("FuelKg", float)
Km = NewType("Km", float)


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


class Step(NamedTuple):
    distance: Km
    emissions: CarbonKg
    fuel_consumption: Optional[FuelKg] = None
