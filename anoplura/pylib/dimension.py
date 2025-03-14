from dataclasses import dataclass


@dataclass(eq=False)
class Dimension:
    dim: str = None
    units: str = None
    low: float = None
    high: float = None
    start: int = None
    end: int = None
