from carbonize.types import CarbonKg, Km, Step

from .base import Calculator


class Train(Calculator):
    """A carbon emissions calculator for railway transport.
    Based on UK GOV carbon conversion factors (kg/km):
    https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2019
    """

    CO2E_PER_KM = 0.04115

    def __init__(self, *, distance: Km) -> None:
        self.distance = distance

    def __repr__(self) -> str:  # pragma: no cover
        return f"Train({self.distance} km)"

    def get_step(self) -> Step:
        return Step(CarbonKg(self.distance * self.CO2E_PER_KM), self.distance, None, self)
