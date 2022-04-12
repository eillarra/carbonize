import pytest

from carbonize.calculators import Train


class TestTrain:
    """The values should be approximate to the results we get at:
    https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx"""

    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.calc = Train(distance=100)

    def test_co2e(self):
        assert self.calc.co2e == 100 * Train.CO2E_PER_KM
