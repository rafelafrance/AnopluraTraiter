from dataclasses import dataclass


@dataclass(eq=False)
class Dim:
    dim: str | None = None
    units: str | None = None
    low: float | None = None
    high: float | None = None
    start: int | None = None
    end: int | None = None
