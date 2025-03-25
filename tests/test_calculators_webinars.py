"""Tests for the Webinar calculator module."""

import pytest

from carbonize.calculators import HostedWebinar, Webinar


class TestWebinar:
    """Tests for the Webinar calculator."""

    @pytest.fixture(autouse=True)
    def setup_data(self):  # noqa: D102
        self.calc = Webinar(duration=60)  # 60 minutes = 1 hour

    def test_co2e_default(self):  # noqa: D102
        # Default is laptop with standard video quality
        assert self.calc.co2e == Webinar.CO2E_PER_HOUR["laptop"]["standard"]
        assert self.calc.co2e_pax == Webinar.CO2E_PER_HOUR["laptop"]["standard"]

    def test_different_device_types(self):  # noqa: D102
        # Test mobile device
        mobile = Webinar(duration=60, device_type="mobile", video_quality="standard")
        assert mobile.co2e == Webinar.CO2E_PER_HOUR["mobile"]["standard"]

        # Test tablet
        tablet = Webinar(duration=60, device_type="tablet", video_quality="standard")
        assert tablet.co2e == Webinar.CO2E_PER_HOUR["tablet"]["standard"]

    def test_different_video_qualities(self):  # noqa: D102
        # Test video off
        video_off = Webinar(duration=60, device_type="laptop", video_quality="video_off")
        assert video_off.co2e == Webinar.CO2E_PER_HOUR["laptop"]["video_off"]

        # Test HD video
        hd = Webinar(duration=60, device_type="laptop", video_quality="hd")
        assert hd.co2e == Webinar.CO2E_PER_HOUR["laptop"]["hd"]

    def test_duration(self):  # noqa: D102
        # Test with different durations
        half_hour = Webinar(duration=30, device_type="laptop", video_quality="standard")
        assert half_hour.co2e == Webinar.CO2E_PER_HOUR["laptop"]["standard"] * 0.5

        two_hours = Webinar(duration=120, device_type="laptop", video_quality="standard")
        assert two_hours.co2e == Webinar.CO2E_PER_HOUR["laptop"]["standard"] * 2

    def test_invalid_parameters(self):  # noqa: D102
        # Should raise ValueError for invalid device type
        with pytest.raises(ValueError):
            Webinar(duration=60, device_type="invalid-device")

        # Should raise ValueError for invalid video quality
        with pytest.raises(ValueError):
            Webinar(duration=60, video_quality="invalid-quality")

    def test_zero_duration(self):  # noqa: D102
        # Test with zero duration
        zero_duration = Webinar(duration=0)
        assert zero_duration.co2e == 0
        assert zero_duration.co2e_pax == 0


class TestHostedWebinar:
    """Tests for the HostedWebinar calculator."""

    @pytest.fixture(autouse=True)
    def setup_data(self):  # noqa: D102
        self.calc = HostedWebinar(duration=60, participants=10)  # 60 minutes = 1 hour

    def test_co2e(self):  # noqa: D102
        # For a hosted webinar, we expect:
        # 1. Host's own device emissions
        # 2. Base hosting emissions
        # 3. Per-participant server emissions
        host_emissions = Webinar(duration=60).co2e
        base_hosting = HostedWebinar.BASE_HOSTING_EMISSIONS
        participant_emissions = HostedWebinar.EMISSIONS_PER_PARTICIPANT["standard"] * 10

        expected_emissions = host_emissions + base_hosting + participant_emissions
        assert self.calc.co2e == pytest.approx(expected_emissions, rel=0.025)
        assert self.calc.co2e_pax == pytest.approx(expected_emissions / 10, rel=0.025)

    def test_different_participant_counts(self):  # noqa: D102
        # Test with different participant counts
        small_meeting = HostedWebinar(duration=60, participants=3)
        large_meeting = HostedWebinar(duration=60, participants=50)

        # Emissions should scale with participant count
        assert small_meeting.co2e < large_meeting.co2e
        assert small_meeting.co2e_pax > large_meeting.co2e_pax  # Per-participant is lower with more participants

    def test_invalid_video_quality(self):  # noqa: D102
        # Test that an invalid video quality raises a ValueError
        with pytest.raises(ValueError, match="Invalid video quality"):
            HostedWebinar(duration=60, participants=10, video_quality="4k")

    def test_zero_participants(self):  # noqa: D102
        # Test with zero participants (should be treated as 1)
        zero_participants = HostedWebinar(duration=60, participants=0)
        one_participant = HostedWebinar(duration=60, participants=1)

        # Both should have the same emissions
        assert zero_participants.co2e == one_participant.co2e
        assert zero_participants.co2e_pax == one_participant.co2e_pax

    def test_negative_participants(self):  # noqa: D102
        # Test with negative participants (should be treated as 1)
        negative_participants = HostedWebinar(duration=60, participants=-5)
        one_participant = HostedWebinar(duration=60, participants=1)

        # Both should have the same emissions
        assert negative_participants.co2e == one_participant.co2e
