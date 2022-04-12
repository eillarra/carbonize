import pytest

from carbonize.api import Footprint


class TestFootprint:
    """The values should be approximate to the results we get at:
    https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx"""

    def test_flight_and_train(self):
        fp = Footprint()
        fp.add_flight(a="BRU", b="BCN")
        fp.add_train(distance=50)
        assert len(fp.steps) == 2
        assert fp.co2e == pytest.approx(116, rel=0.025)

    def test_two_ways(self):
        fp = Footprint()
        fp.add_flight(a="BRU", b="BCN", two_way=True)
        fp.add_train(distance=50, two_way=True)
        assert len(fp.steps) == 4
        assert fp.co2e == pytest.approx(116 * 2, rel=0.025)
