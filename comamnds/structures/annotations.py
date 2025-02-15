import dataclasses


@dataclasses.dataclass
class MaxLen:
    value: int

@dataclasses.dataclass
class ValueRange:
    lo: int
    hi: int


