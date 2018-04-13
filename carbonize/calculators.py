from .catalogs import AircraftCatalog, AirportCatalog
from .utils import great_circle
from .typing import Airport, CarbonEmissions, Km


class Calculator:
    distance: Km = None
    emissions: CarbonEmissions = None

    def __init__(self):
        self.load_data()

    def calculate(self, origin, destination) -> None:
        raise NotImplemented


class AviationCalculator(Calculator):
    """A carbon emissions calculator for aviation.
    """
    def load_data(self) -> None:
        self.aircrafts = AircraftCatalog()
        self.airports = AirportCatalog()

    def calculate_distance(self, a_airport: Airport, b_airport: Airport) -> Km:
        """Given origin and destination Airports, the GCD is calculated and then corrected by a factor:
        - Less than 550 Km: +50 Km
        - Between 550 Km and 5500 Km: +100 Km
        - Above 5500 Km: + 125 Km
        """
        km = great_circle(a_airport.point, b_airport.point)

        for correction_factor in [(5500, 125), (550, 100), (0, 50)]:
            if km > correction_factor[0]:
                return km + correction_factor[1]

    def calculate_emissions(self, distance: Km, aircraft: str) -> CarbonEmissions:
        raise NotImplemented

    def calculate(self, origin: str, destination: str, aircraft: str = AircraftCatalog.DEFAULT) -> None:
        a_airport, b_airport = self.airports.get(origin), self.airports.get(destination)
        self.distance = self.calculate_distance(a_airport, b_airport)
        self.emissions = self.calculate_emissions(self.distance, aircraft)
