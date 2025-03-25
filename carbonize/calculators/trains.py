"""Train carbon emissions calculator."""

from carbonize.type_definitions import CO2e, Km, Step

from .base import Calculator


class Train(Calculator):
    """A carbon emissions calculator for railway transport.

    Based on UK DEFRA greenhouse gas reporting conversion factors.
    Source: https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2022
    """

    # CO2e emissions values in kg CO2e per passenger-kilometer
    CO2E_PER_KM = {
        "local": 0.0369,  # National rail average
        "intercity": 0.0354,  # International rail
        "highspeed": 0.0042,  # Eurostar
        "underground": 0.0275,  # London Underground
        "tram": 0.0302,  # Light rail and tram
    }

    def __init__(self, *, distance: Km, train_type: str = "local", passengers: int = 1) -> None:
        """Initialize a Train calculator.

        :param distance: Distance in kilometers.
        :param train_type: Type of train.
        :param passengers: Number of passengers traveling.
        """
        self.distance = distance
        self.train_type = train_type
        self.passengers = max(1, passengers)  # Ensure at least 1 passenger

        if self.train_type not in self.CO2E_PER_KM:
            raise ValueError(f"Invalid train type: {self.train_type}. Valid types: {list(self.CO2E_PER_KM.keys())}")

    def __repr__(self) -> str:
        """Return a string representation of the Train trip."""
        return f"Train({self.distance} km, {self.train_type}, {self.passengers} passenger(s))"

    @property
    def co2e(self) -> CO2e:
        """The total CO2e for the train journey."""
        # Train emission factors already account for average occupancy,
        # so we multiply by passengers to get total emissions
        return CO2e(self.CO2E_PER_KM[self.train_type] * self.distance * self.passengers)

    @property
    def co2e_pax(self) -> CO2e:
        """The CO2e per passenger for the train journey."""
        # Since emission factors are already per passenger, we can directly use them
        return CO2e(self.CO2E_PER_KM[self.train_type] * self.distance)

    def get_step(self) -> Step:
        """Return the CO2e step for the train trip."""
        return Step(self.co2e_pax, self.distance, None, self)
