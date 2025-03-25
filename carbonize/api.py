"""Module containing the main API of the package."""

from carbonize.calculators import Flight, HostedWebinar, Ride, Train, Webinar
from carbonize.type_definitions import CO2e, Km, Step


class Footprint:
    """The footprint is an object that stores different emission steps.

    Each step is linked to a CO2e calculator.
    """

    steps: list[Step]

    def __init__(self):
        """Initialize a Footprint."""
        self.steps = []

    def add_flight(self, *, a: str, b: str, two_way: bool = False, aircraft: str = Flight.DEFAULT_AIRCRAFT) -> None:
        """Add a flight to the footprint.

        :param a: Origin airport IATA code.
        :param b: Destination airport IATA code.
        :param two_way: Add a return flight.
        :param aircraft: Aircraft ICAO code.
        """
        self.steps.append(Flight(a=a, b=b, aircraft=aircraft).get_step())

        if two_way:
            self.add_flight(a=b, b=a, aircraft=aircraft)

    def add_ride(
        self,
        *,
        distance: Km,
        vehicle_type: str = "medium-plugin-hybrid-car",
        passengers: int = 1,
        two_way: bool = False,
    ) -> None:
        """Add a car ride to the footprint.

        :param distance: Distance in kilometers.
        :param vehicle_type: Vehicle type.
        :param passengers: Number of passengers in the vehicle.
        :param two_way: Add a return ride.
        """
        self.steps.append(Ride(distance=distance, vehicle_type=vehicle_type, passengers=passengers).get_step())

        if two_way:
            self.add_ride(distance=distance, vehicle_type=vehicle_type, passengers=passengers)

    def add_train(self, *, distance: Km, train_type: str = "local", passengers: int = 1, two_way: bool = False) -> None:
        """Add a train trip to the footprint.

        :param distance: Distance in kilometers.
        :param train_type: Type of train.
        :param passengers: Number of passengers traveling.
        :param two_way: Add a return trip.
        """
        self.steps.append(Train(distance=distance, train_type=train_type, passengers=passengers).get_step())

        if two_way:
            self.add_train(distance=distance, train_type=train_type, passengers=passengers)

    def add_webinar(
        self,
        *,
        duration: int,
        device_type: str = "laptop",
        video_quality: str = "standard",
        hosted: bool = False,
        participants: int = 1,
    ) -> None:
        """Add a webinar to the footprint.

        :param duration: Duration in minutes.
        :param device_type: Device used (laptop, mobile, or tablet).
        :param video_quality: Video quality (video_off, standard, or hd).
        :param hosted: Whether this is a hosted webinar (default: False).
        :param participants: Number of participants (only for hosted webinars).
        """
        if hosted:
            self.steps.append(
                HostedWebinar(
                    duration=duration, device_type=device_type, video_quality=video_quality, participants=participants
                ).get_step()
            )
        else:
            self.steps.append(
                Webinar(duration=duration, device_type=device_type, video_quality=video_quality).get_step()
            )

    @property
    def co2e(self) -> CO2e:
        """Return the total CO2e or total footprint."""
        if not self.steps:
            return CO2e(0)
        return CO2e(sum([step.co2e for step in self.steps]))
