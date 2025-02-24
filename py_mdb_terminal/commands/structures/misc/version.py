import dataclasses


@dataclasses.dataclass
class Version:
    COMMAND = b"V"

    software_version: str
    cpu_id: str