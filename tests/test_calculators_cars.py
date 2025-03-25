"""Tests for the Ride calculator module."""

import pytest

from carbonize.calculators import Ride


class TestRide:
    """Tests for the Ride calculator."""

    @pytest.fixture(autouse=True)
    def setup_data(self):  # noqa: D102
        self.calc = Ride(distance=100)  # 100 km with default vehicle type

    def test_co2e_default(self):  # noqa: D102
        # Default is medium-plugin-hybrid-car with 1 passenger
        assert self.calc.co2e == 100 * Ride.CO2E_PER_KM["medium-plugin-hybrid-car"]
        assert self.calc.co2e_pax == 100 * Ride.CO2E_PER_KM["medium-plugin-hybrid-car"]

    def test_different_vehicle_types(self):  # noqa: D102
        # Test small diesel
        small_diesel = Ride(distance=100, vehicle_type="small-diesel-car")
        assert small_diesel.co2e == 100 * Ride.CO2E_PER_KM["small-diesel-car"]

        # Test large electric
        large_electric = Ride(distance=100, vehicle_type="large-electric-car")
        assert large_electric.co2e == 100 * Ride.CO2E_PER_KM["large-electric-car"]

        # Test bus
        bus = Ride(distance=100, vehicle_type="bus")
        assert bus.co2e == 100 * Ride.CO2E_PER_KM["bus"]

    def test_multiple_passengers(self):  # noqa: D102
        # With multiple passengers, the per-passenger CO2e should be divided
        single_passenger = Ride(distance=100, vehicle_type="medium-petrol-car", passengers=1)
        multi_passenger = Ride(distance=100, vehicle_type="medium-petrol-car", passengers=4)

        # Total emissions remain the same
        assert single_passenger.co2e == multi_passenger.co2e
        # Per-passenger emissions are divided by passenger count
        assert single_passenger.co2e_pax == 4 * multi_passenger.co2e_pax

    def test_bike(self):  # noqa: D102
        # Bike should have zero emissions
        bike = Ride(distance=100, vehicle_type="bike")
        assert bike.co2e == 0
        assert bike.co2e_pax == 0

    def test_invalid_vehicle_type(self):  # noqa: D102
        # Should raise ValueError for invalid vehicle type
        with pytest.raises(ValueError):
            Ride(distance=100, vehicle_type="invalid-vehicle")
