import pytest

from carbonize.calculators import Flight
from carbonize.utils import great_circle


class TestFlight:
    """The values should be approximate to the results we get at:
    https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx"""

    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.calc = Flight(a="BRU", b="BCN")

    def test_distance(self):
        gc = great_circle(self.calc.a.point, self.calc.b.point)
        assert self.calc.get_step().distance == (gc + 100)
        assert self.calc.get_step().distance == pytest.approx(1185, rel=0.025)

    def test_fuel_consumption(self):
        assert self.calc.get_step().fuel_consumption == pytest.approx(5412, rel=0.025)

    def test_emissions_pax(self):
        assert self.calc.get_step().co2e == pytest.approx(116, rel=0.025)
