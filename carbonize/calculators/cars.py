"""Car carbon emissions calculator."""

from carbonize.type_definitions import CO2e, Km, Step

from .base import Calculator


class Ride(Calculator):
    """A carbon emissions calculator for car/bus rides."""

    CO2E_PER_KM = {
        "small-diesel-car": 0.142,
        "small-petrol-car": 0.154,
        "small-plugin-hybrid-car": 0.073,
        "small-electric-car": 0.027,
        "medium-diesel-car": 0.171,
        "medium-petrol-car": 0.192,
        "medium-plugin-hybrid-car": 0.11,
        "medium-electric-car": 0.073,
        "large-diesel-car": 0.209,
        "large-petrol-car": 0.282,
        "large-plugin-hybrid-car": 0.126,
        "large-electric-car": 0.073,
        "bus": 0.089,
        "bike": 0,  # so just use your bike!
    }

    def __init__(self, *, distance: Km, vehicle_type: str = "medium-plugin-hybrid-car", passengers: int = 1) -> None:
        """Initialize a Ride calculator.

        :param distance: Distance in kilometers.
        :param vehicle_type: Vehicle type.
        :param passengers: Number of passengers in the vehicle (default: 1).
        """
        self.distance = distance
        self.vehicle_type = vehicle_type
        self.passengers = max(1, passengers)  # Ensure at least 1 passenger

        if self.vehicle_type not in self.CO2E_PER_KM:
            raise ValueError(f"Invalid vehicle type: {self.vehicle_type}. Valid types: {list(self.CO2E_PER_KM.keys())}")

    def __repr__(self) -> str:
        """Return a string representation of the Ride."""
        return f"Ride({self.distance} km, {self.passengers} passenger(s))"

    @property
    def co2e(self) -> CO2e:
        """The total CO2e for the ride."""
        return CO2e(self.CO2E_PER_KM[self.vehicle_type] * self.distance)

    @property
    def co2e_pax(self) -> CO2e:
        """The CO2e per passenger for the ride."""
        return CO2e(self.co2e / self.passengers)

    def get_step(self) -> Step:
        """Return the CO2e step for the ride."""
        return Step(self.co2e_pax, self.distance, None, self)
