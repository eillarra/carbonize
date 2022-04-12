from carbonize.types import CarbonKg, Step


class Calculator:
    @property
    def co2e(self) -> CarbonKg:
        return self.get_step().co2e

    def get_step(self) -> Step:
        raise NotImplementedError
