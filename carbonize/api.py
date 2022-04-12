from typing import List

from carbonize.calculators import Flight, Train
from carbonize.types import CarbonKg, Km, Step


class Footprint:
    """The footprint is an object that stores different emission steps.
    Each step is linked to a CO2e calculator.
    """

    def __init__(self):
        self.steps: List[Step] = []

    def add_flight(self, *, a: str, b: str, two_way: bool = False, aircaft: str = Flight.DEFAULT_AIRCRAFT) -> None:
        self.steps.append(Flight(a=a, b=b).get_step())

        if two_way:
            self.add_flight(a=b, b=a, aircaft=aircaft)

    def add_train(self, *, distance: Km, two_way: bool = False) -> None:
        self.steps.append(Train(distance=distance).get_step())

        if two_way:
            self.add_train(distance=distance)

    @property
    def co2e(self) -> CarbonKg:
        return CarbonKg(sum([step.co2e for step in self.steps]))
