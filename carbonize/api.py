from typing import List

from carbonize.calculators import FlightCalculator, TrainCalculator
from carbonize.types import CarbonKg, Km, Step


class Footprint:
    _c_flight: FlightCalculator = FlightCalculator()
    _c_train: TrainCalculator = TrainCalculator()

    def __init__(self):
        self.steps: List[Step] = []

    def add_flight(self, *, a: str, b: str, two_way: bool = False) -> None:
        step = self._c_flight.calculate(a=a, b=b)
        self.steps.append(step)

        if two_way:
            self.add_flight(a=b, b=a)

    def add_train(self, *, distance: Km, two_way: bool = False) -> None:
        step = self._c_train.calculate(distance=distance)
        self.steps.append(step)

        if two_way:
            self.add_train(distance=distance)

    @property
    def emissions(self) -> CarbonKg:
        return CarbonKg(sum([step.emissions for step in self.steps]))
