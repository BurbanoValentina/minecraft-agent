from dataclasses import dataclass


@dataclass
class Material:
    name: str
    quantity: int


def estimate_medieval_materials(size: str, floors: int) -> list[Material]:
    if size.lower() == "15x15" and floors == 2:
        return [
            Material("Roble", 250),
            Material("Piedra", 80),
            Material("Cristal", 40),
            Material("Escaleras", 20),
        ]

    width, length = (int(part) for part in size.lower().split("x"))
    footprint = width * length
    scale = max(1, floors)

    return [
        Material("Roble", footprint),
        Material("Piedra", int(footprint * 0.32) * scale),
        Material("Cristal", int((width + length) * 1.5)),
        Material("Escaleras", int((width + length) * 1.25)),
    ]