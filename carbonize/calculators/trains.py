from carbonize.types import CarbonKg, Km, Step

from .base import Calculator


class TrainCalculator(Calculator):
    """A carbon emissions calculator for railway transport.
    Based on UK GOV carbon conversion factors (kg/km):
    https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2019
    """

    CO2E_PER_KM = 0.04115

    def calculate(self, *, distance: Km) -> Step:
        return Step(distance, CarbonKg(distance * self.CO2E_PER_KM))
