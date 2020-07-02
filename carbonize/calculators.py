from .catalogs import AircraftCatalog, AirportCatalog
from .utils import great_circle
from .types import CarbonKg, FuelKg, Km, Route, Step


class Calculator:
    pass


class FlightCalculator(Calculator):
    """A carbon emissions calculator for flights.
    """

    aircrafts = AircraftCatalog()
    airports = AirportCatalog()

    DEFAULT_ROUTE = Route(25, "Intra Europe", 80.89, 96.23)  # TODO

    def calculate(
        self, *, a: str, b: str, aircraft: str = AircraftCatalog.DEFAULT
    ) -> Step:
        self.a, self.b = self.airports.get(a), self.airports.get(b)
        self.aircraft = self.aircrafts.get(aircraft)
        return Step(self.distance, self.emissions_pax, self.fuel_consumption)

    @property
    def distance(self) -> Km:
        """Given origin and destination Airports, the GCD is calculated and then corrected by a factor:
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
        """For flights longer than 5000 Km, we are assuming a stop will be needed.
        """
        if self.distance > 5000:
            return FuelKg(
                self.aircrafts.get_consumption(
                    Km(self.distance / 2), AircraftCatalog.DEFAULT_LONG_DISTANCE
                )
                * 2
            )
        return self.aircrafts.get_consumption(self.distance, self.aircraft.code)

    @property
    def emissions_pax(self) -> CarbonKg:
        r = self.DEFAULT_ROUTE
        return CarbonKg(
            3.16
            * (self.fuel_consumption * r.pax_to_freight_factor)
            / (self.aircraft.y_seats * r.pax_load_factor)
        )


class TrainCalculator(Calculator):
    """A carbon emissions calculator for railway transport.
    Based on UK GOV carbon conversion factors (kg/km):
    https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2019
    """

    CO2E_PER_KM = 0.04115

    def calculate(self, *, distance: Km) -> Step:
        return Step(distance, CarbonKg(distance * self.CO2E_PER_KM))
