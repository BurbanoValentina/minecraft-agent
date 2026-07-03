from dataclasses import dataclass, field


@dataclass
class HouseBlueprint:
    title: str
    style: str
    size: str
    floors: int
    rooms: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)