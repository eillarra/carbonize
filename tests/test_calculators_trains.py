"""Tests for the Train calculator module."""

import pytest

from carbonize.calculators import Train


class TestTrain:
    """Tests for the Train calculator."""

    @pytest.fixture(autouse=True)
    def setup_data(self):  # noqa: D102
        self.calc = Train(distance=100)

    def test_co2e_default(self):  # noqa: D102
        # Using default parameters (local train, 1 passenger)
        assert self.calc.co2e == 100 * Train.CO2E_PER_KM["local"]
        assert self.calc.co2e_pax == 100 * Train.CO2E_PER_KM["local"]

    def test_different_train_types(self):  # noqa: D102
        # Test high-speed train
        highspeed = Train(distance=100, train_type="highspeed")
        assert highspeed.co2e == 100 * Train.CO2E_PER_KM["highspeed"]

        # Test underground
        underground = Train(distance=100, train_type="underground")
        assert underground.co2e == 100 * Train.CO2E_PER_KM["underground"]

    def test_multiple_passengers(self):  # noqa: D102
        # With multiple passengers, the total CO2e should be multiplied
        # but per-passenger emissions remain the same
        multi_passenger = Train(distance=100, train_type="local", passengers=3)
        assert multi_passenger.co2e == 100 * Train.CO2E_PER_KM["local"] * 3
        assert multi_passenger.co2e_pax == 100 * Train.CO2E_PER_KM["local"]

    def test_invalid_train_type(self):  # noqa: D102
        # Should raise ValueError for invalid train type
        with pytest.raises(ValueError):
            Train(distance=100, train_type="invalid-type")
