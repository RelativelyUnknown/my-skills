from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Discount:
    rate: float

    def __post_init__(self):
        if not 0 <= self.rate <= 1:
            raise ValueError("rate must be between 0 and 1")
