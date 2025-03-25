"""Module for type definitions."""

import bisect
from typing import TYPE_CHECKING, NamedTuple, NewType, Optional


if TYPE_CHECKING:  # pragma: no cover
    from carbonize.calculators.base import Calculator


CO2e = NewType("CO2e", float)
FuelKg = NewType("FuelKg", float)
Km = NewType("Km", float)


class Point(NamedTuple):
    """A geographical point.

    :param latitude: The latitude of the point, in degrees. Must be between -90 and 90.
    :param longitude: The longitude of the point, in degrees. Must be between -180 and 180.
    """

    latitude: float
    longitude: float

    def __init_subclass__(cls, latitude, longitude):
        """Validate latitude and longitude values."""
        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid latitude value. It should be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid longitude value. It should be between -180 and 180.")


class Aircraft(NamedTuple):
    """An aircraft.

    :param code: ICAO code.
    :param fuel_consumption: Fuel consumption data per nautical mile.
    :param y_seats: Number of seats in economy class.
    """

    code: str
    fuel_consumption: list[int | None]
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
    """An airport.

    :param code: IATA code.
    :param country: Country name.
    :param city: City name.
    :param latitude: Latitude of the airport.
    :param longitude: Longitude of the airport.
    """

    code: str
    country: str
    city: str
    latitude: float
    longitude: float

    @property
    def point(self) -> Point:
        """Return the geographical point of the airport."""
        return Point(self.latitude, self.longitude)


class Route(NamedTuple):
    """A flight route.

    :param code: Route code.
    :param name: Route name.
    :param pax_load_factor: Passenger load factor.
    :param pax_to_freight_factor: Passenger to freight factor.
    """

    code: int
    name: str
    pax_load_factor: float
    pax_to_freight_factor: float


class Step(NamedTuple):
    """A step in a carbon emissions calculation.

    :param co2e: CO2e in Kg.
    :param distance: Distance in kilometers.
    :param fuel_consumption: Fuel consumption in Kg.
    :param calculator: The calculator that generated this step.
    """

    co2e: CO2e
    distance: Km
    fuel_consumption: Optional[FuelKg] = None
    calculator: Optional["Calculator"] = None

    def __add__(self: tuple, other: tuple) -> tuple:
        """Add two steps together."""
        step1, step2 = Step(*self), Step(*other)

        return (
            step1.co2e + step2.co2e,
            step1.distance + step2.distance,
        )
