"""Flight calculator."""

from carbonize.catalogs import AircraftCatalog, AirportCatalog
from carbonize.type_definitions import CO2e, FuelKg, Km, Route, Step
from carbonize.utils import great_circle

from .base import Calculator


class Flight(Calculator):
    """A carbon emissions calculator for flights."""

    DEFAULT_AIRCRAFT = AircraftCatalog.DEFAULT
    DEFAULT_ROUTE = Route(25, "Intra Europe", 80.89, 96.23)  # TODO

    aircrafts = AircraftCatalog()
    airports = AirportCatalog()

    def __init__(self, *, a: str, b: str, aircraft: str = AircraftCatalog.DEFAULT) -> None:
        """Initialize a Flight calculator.

        :param a: Origin airport IATA code.
        :param b: Destination airport IATA code.
        :param aircraft: Aircraft ICAO code.
        """
        self.a, self.b = self.airports.get(a), self.airports.get(b)
        self.aircraft = self.aircrafts.get(aircraft)

    def __repr__(self) -> str:
        """Return a string representation of the Flight."""
        return f"Flight({self.a.code}-{self.b.code}, {self.distance} km)"

    @property
    def co2e_pax(self) -> CO2e:
        """The CO2e per passenger for the flight."""
        r = self.DEFAULT_ROUTE
        return CO2e(
            3.16 * (self.fuel_consumption * r.pax_to_freight_factor) / (self.aircraft.y_seats * r.pax_load_factor)
        )

    @property
    def distance(self) -> Km:
        """The distance between the two airports.

        The GCD is calculated and then corrected by a factor:
        - Less than 550 Km: +50 Km
        - Between 550 Km and 5500 Km: +100 Km
        - Above 5500 Km: + 125 Km
        """
        km = great_circle(self.a.point, self.b.point)
        distance: Km = km

        for correction_factor in [(5500, 125), (550, 100), (0, 50)]:
            if km > correction_factor[0]:
                distance = Km(km + correction_factor[1])
                break

        return distance

    @property
    def fuel_consumption(self) -> FuelKg:
        """The fuel consumption for the flight.

        For flights longer than 5000 Km, we are assuming a stop will be needed.
        """
        try:
            return self.aircraft.get_consumption(self.distance)
        except IndexError:
            return FuelKg(self.aircraft.get_consumption(Km(self.distance / 2)) * 2)

    def get_step(self) -> Step:
        """Return the CO2e step for the flight."""
        return Step(self.co2e_pax, self.distance, self.fuel_consumption, self)
