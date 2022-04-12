import pytest

from carbonize.api import Footprint


class TestFootprint:
    """The values should be approximate to the results we get at:
    https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx"""

    def test_flight(self):
        fp = Footprint()
        fp.add_flight(a="BRU", b="BCN")
        assert len(fp.steps) == 1
        assert fp.emissions == pytest.approx(116, rel=0.025)

    def test_flight_two_way(self):
        fp = Footprint()
        fp.add_flight(a="BRU", b="BCN", two_way=True)
        assert len(fp.steps) == 2
        assert fp.emissions == pytest.approx(116 * 2, rel=0.025)
