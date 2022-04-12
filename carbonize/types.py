import bisect

from typing import List, NamedTuple, NewType, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from carbonize.calculators.base import Calculator


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

    def get_consumption(self, distance: Km) -> FuelKg:
        """ICAO fuel consumption data is given per nautical mile, so we need to transform the ranges to Km first."""

        miles = "125 250 500 750 1000 1500 2000 2500 3000 3500 4000 4500 5000 5500 6000 6500 7000 7500 8000 8500"
        ranges = [int(nm) * 1.852 for nm in miles.split()]
        idx = bisect.bisect_left(ranges, distance)
        fuel_consumption = self.fuel_consumption[idx]

        if not fuel_consumption:
            raise IndexError(f"No fuel consumption data for {self.code} at {distance} Km.")

        return FuelKg((fuel_consumption / ranges[idx]) * distance)


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
    co2e: CarbonKg
    distance: Km
    fuel_consumption: Optional[FuelKg] = None
    calculator: Optional["Calculator"] = None
