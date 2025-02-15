import dataclasses


@dataclasses.dataclass
class Hardware:
    COMMAND = b"H"

    hardware_version: str
    capabilities: str