from .catalogs import AircraftCatalog, AirportCatalog
from .utils import great_circle
from .typing import CarbonKg, FuelKg, Km, Route


class AviationCalculator:
    DEFAULT_ROUTE = Route(25, 'Intra Europe', 80.89, 96.23)  # TODO

    """A carbon emissions calculator for aviation.
    """
    def __init__(self, origin: str, destination: str, aircraft_code: str = AircraftCatalog.DEFAULT) -> None:
        airports = AirportCatalog()
        self.a, self.b = airports.get(origin), airports.get(destination)
        self.aircrafts = AircraftCatalog()
        self.aircraft = self.aircrafts.get(aircraft_code)

    @property
    def distance(self) -> Km:
        """Given origin and destination Airports, the GCD is calculated and then corrected by a factor:
        - Less than 550 Km: +50 Km
        - Between 550 Km and 5500 Km: +100 Km
        - Above 5500 Km: + 125 Km
        """
        km = great_circle(self.a.point, self.b.point)

        for correction_factor in [(5500, 125), (550, 100), (0, 50)]:
            if km > correction_factor[0]:
                return km + correction_factor[1]

    @property
    def fuel_consumption(self) -> FuelKg:
        if self.distance > 5000:
            return self.aircrafts.get_consumption(self.distance / 2, AircraftCatalog.DEFAULT_LONG_DISTANCE) * 2
        return self.aircrafts.get_consumption(self.distance, self.aircraft.code)

    @property
    def emissions_pax(self) -> CarbonKg:
        r = self.DEFAULT_ROUTE
        return 3.16 * (self.fuel_consumption * r.pax_to_freight_factor) / (self.aircraft.y_seats * r.pax_load_factor)
