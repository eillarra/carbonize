"""Calculators for online webinars."""

from carbonize.type_definitions import CO2e, Step

from .base import Calculator


class Webinar(Calculator):
    """A carbon emissions calculator for attending online webinars.

    Based on studies including:
    - https://blog.zoom.us/how-video-meetings-are-helping-reduce-environmental-impact-infographic/
    - https://www.carbontrust.com/resources/carbon-impact-of-video-streaming
    """

    # CO2e emissions in kg per hour of video conferencing
    # Values vary by video quality and device
    CO2E_PER_HOUR = {
        # Laptop/desktop values
        "laptop": {
            "video_off": 0.08,  # Audio only
            "standard": 0.15,  # Standard definition video
            "hd": 0.23,  # High definition video
        },
        # Mobile device values
        "mobile": {
            "video_off": 0.04,  # Audio only
            "standard": 0.09,  # Standard definition video
            "hd": 0.13,  # High definition video
        },
        # Tablet values
        "tablet": {
            "video_off": 0.06,  # Audio only
            "standard": 0.11,  # Standard definition video
            "hd": 0.17,  # High definition video
        },
    }

    def __init__(self, *, duration: int, device_type: str = "laptop", video_quality: str = "standard") -> None:
        """Initialize a Webinar calculator for attendees.

        :param duration: Duration in minutes.
        :param device_type: Device used (laptop, mobile, or tablet).
        :param video_quality: Video quality (video_off, standard, or hd).
        """
        self.duration = duration
        self.device_type = device_type
        self.video_quality = video_quality

        if self.device_type not in self.CO2E_PER_HOUR:
            raise ValueError(f"Invalid device type: {self.device_type}. Valid types: {list(self.CO2E_PER_HOUR.keys())}")

        if self.video_quality not in self.CO2E_PER_HOUR[self.device_type]:
            raise ValueError(
                f"Invalid video quality: {self.video_quality}. "
                f"Valid qualities: {list(self.CO2E_PER_HOUR[self.device_type].keys())}"
            )

    def __repr__(self) -> str:
        """Return a string representation of the Webinar."""
        return f"Webinar({self.duration} minutes, {self.device_type}, {self.video_quality})"

    @property
    def co2e(self) -> CO2e:
        """The CO2e for attending the webinar."""
        # Convert duration from minutes to hours
        hours = self.duration / 60
        return CO2e(self.CO2E_PER_HOUR[self.device_type][self.video_quality] * hours)

    @property
    def co2e_pax(self) -> CO2e:
        """The CO2e per person for the webinar."""
        return self.co2e  # For attendee, personal footprint equals total

    def get_step(self) -> Step:
        """Return the CO2e step for the webinar."""
        return Step(self.co2e, None, None, self)


class HostedWebinar(Calculator):
    """A carbon emissions calculator for hosting online webinars.

    Includes both host emissions and server-side emissions to support all participants.
    """

    # Base emissions for hosting (kg CO2e per hour)
    BASE_HOSTING_EMISSIONS = 0.25  # Higher than attending due to additional processing

    # Additional emissions per participant (kg CO2e per person-hour)
    EMISSIONS_PER_PARTICIPANT = {
        "video_off": 0.02,  # Audio only
        "standard": 0.04,  # Standard definition video
        "hd": 0.07,  # High definition video
    }

    def __init__(
        self, *, duration: int, participants: int = 10, device_type: str = "laptop", video_quality: str = "standard"
    ) -> None:
        """Initialize a HostedWebinar calculator.

        :param duration: Duration in minutes.
        :param participants: Number of participants (including host).
        :param device_type: Host's device (laptop, mobile, or tablet).
        :param video_quality: Video quality (video_off, standard, or hd).
        """
        self.duration = duration
        self.participants = max(1, participants)  # At least 1 participant (the host)
        self.device_type = device_type
        self.video_quality = video_quality

        # Use the Webinar calculator for the host's own device emissions
        self.host_calculator = Webinar(duration=duration, device_type=device_type, video_quality=video_quality)

        if self.video_quality not in self.EMISSIONS_PER_PARTICIPANT:
            raise ValueError(
                f"Invalid video quality: {self.video_quality}. "
                f"Valid qualities: {list(self.EMISSIONS_PER_PARTICIPANT.keys())}"
            )

    def __repr__(self) -> str:
        """Return a string representation of the HostedWebinar."""
        return f"HostedWebinar({self.duration} minutes, {self.participants} participants, {self.video_quality})"

    @property
    def co2e(self) -> CO2e:
        """The total CO2e for hosting the webinar."""
        # Convert duration from minutes to hours
        hours = self.duration / 60

        # Host's own device emissions + base hosting emissions + per-participant server emissions
        host_emissions = self.host_calculator.co2e
        base_hosting = CO2e(self.BASE_HOSTING_EMISSIONS * hours)
        participant_emissions = CO2e(self.EMISSIONS_PER_PARTICIPANT[self.video_quality] * hours * self.participants)

        return CO2e(host_emissions + base_hosting + participant_emissions)

    @property
    def co2e_pax(self) -> CO2e:
        """The CO2e per participant for the hosted webinar."""
        return CO2e(self.co2e / self.participants)

    def get_step(self) -> Step:
        """Return the CO2e step for the hosted webinar."""
        return Step(self.co2e, None, None, self)
