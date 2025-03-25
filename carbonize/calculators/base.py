"""Base class for carbon calculators."""

from carbonize.type_definitions import CO2e, Step


class Calculator:
    """A carbon emissions calculator."""

    @property
    def co2e(self) -> CO2e:
        """Calculate the CO2e for the calculator."""
        return self.get_step().co2e

    def get_step(self) -> Step:
        """Return the CO2e step for the calculator."""
        raise NotImplementedError
