"""Tests for the carbonize API."""

import pytest

from carbonize.api import Footprint


class TestFootprint:
    """The values should be approximate to the results we get at.

    https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx
    """

    def test_flight_and_train(self):  # noqa: D102
        fp = Footprint()
        fp.add_flight(a="BRU", b="BCN")
        fp.add_train(distance=50, train_type="local", passengers=1)
        assert len(fp.steps) == 2
        assert fp.co2e == pytest.approx(116 + 50 * 0.0369, rel=0.025)

    def test_two_ways(self):  # noqa: D102
        fp = Footprint()
        fp.add_flight(a="BRU", b="BCN", two_way=True)
        fp.add_train(distance=50, train_type="highspeed", two_way=True, passengers=1)
        assert len(fp.steps) == 4
        assert fp.co2e == pytest.approx(116 * 2 + 50 * 0.0042 * 2, rel=0.025)

    def test_ride(self):  # noqa: D102
        fp = Footprint()
        fp.add_ride(distance=100, vehicle_type="medium-petrol-car", passengers=2)
        assert len(fp.steps) == 1
        # With 2 passengers, emissions per passenger are halved
        assert fp.co2e == pytest.approx(100 * 0.192 / 2, rel=0.025)

    def test_webinar(self):  # noqa: D102
        fp = Footprint()
        fp.add_webinar(duration=60, device_type="laptop", video_quality="standard")
        assert len(fp.steps) == 1
        # 60 minutes = 1 hour, standard quality on laptop = 0.15 kg CO2e per hour
        assert fp.co2e == pytest.approx(0.15, rel=0.025)

    def test_all_calculators(self):  # noqa: D102
        fp = Footprint()
        fp.add_flight(a="BRU", b="BCN")
        fp.add_train(distance=50, train_type="highspeed", passengers=1)
        fp.add_ride(distance=100, vehicle_type="medium-petrol-car", passengers=2)
        fp.add_webinar(duration=60, device_type="laptop", video_quality="standard")
        assert len(fp.steps) == 4
        expected_co2e = (
            116  # Flight emissions (approx)
            + 50 * 0.0042  # Train emissions (highspeed)
            + 100 * 0.192 / 2  # Car emissions with 2 passengers
            + 0.15  # Webinar emissions (1 hour, standard quality)
        )
        assert fp.co2e == pytest.approx(expected_co2e, rel=0.025)

    def test_import_via_init(self):  # noqa: D102
        # Test that the Footprint class can be imported directly from the package
        from carbonize import Footprint

        fp = Footprint()
        assert len(fp.steps) == 0
        assert fp.co2e == 0

    def test_hosted_webinar(self):  # noqa: D102
        # Test adding a hosted webinar which uses different calculator
        fp = Footprint()
        fp.add_webinar(duration=60, device_type="laptop", video_quality="standard", hosted=True, participants=5)
        assert len(fp.steps) == 1

        # HostedWebinar should have higher emissions than regular Webinar
        regular_webinar = Footprint()
        regular_webinar.add_webinar(duration=60, device_type="laptop", video_quality="standard")

        assert fp.co2e > regular_webinar.co2e
