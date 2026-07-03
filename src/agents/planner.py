from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from src.agents.architect import HouseBlueprint
from src.agents.materials import estimate_medieval_materials

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "architect_prompt.txt"


@dataclass
class MinecraftPlan:
    title: str
    size: str
    materials: list[dict[str, int | str]]
    floors: int
    rooms: list[str]
    summary: str
    ascii_plan: str
    notes: list[str]

    def model_dump(self) -> dict[str, object]:
        return asdict(self)


def _fallback_blueprint(user_request: str) -> HouseBlueprint:
    text = user_request.lower()

    if "medieval" in text:
        return HouseBlueprint(
            title="Casa Medieval",
            style="medieval",
            size="15x15",
            floors=2,
            rooms=["Sala", "Dormitorio", "Almacén", "Encantamientos"],
            notes=["Ideal para supervivencia", "Incluye techo alto y torres pequeñas"],
        )

    if "casa" in text:
        return HouseBlueprint(
            title="Casa de Supervivencia",
            style="survival",
            size="12x12",
            floors=1,
            rooms=["Sala", "Dormitorio", "Almacén"],
            notes=["Diseño compacto para empezar rápido"],
        )

    return HouseBlueprint(
        title="Refugio Base",
        style="general",
        size="10x10",
        floors=1,
        rooms=["Sala", "Almacén"],
        notes=["Base simple y funcional"],
    )


def _compact_summary(blueprint: HouseBlueprint, materials: list[dict[str, int | str]]) -> str:
    materials_text = " ".join(f"{item['quantity']} {item['name']}" for item in materials)
    rooms_text = " ".join(blueprint.rooms)
    return (
        f"{blueprint.title}"
        f"Tamaño:{blueprint.size}"
        f"Materiales:{materials_text}"
        f"Pisos:{blueprint.floors}"
        f"Habitaciones:{rooms_text}"
    )


def _ascii_plan(blueprint: HouseBlueprint) -> str:
    width = 15 if blueprint.size == "15x15" else 12 if blueprint.size == "12x12" else 10
    border = "+" + "-" * width + "+"
    middle = "|" + "Casa".center(width) + "|"
    return "\n".join([border, middle, border])


def generate_plan(user_request: str) -> MinecraftPlan:
    blueprint = _fallback_blueprint(user_request)
    materials = [
        {"name": material.name, "quantity": material.quantity}
        for material in estimate_medieval_materials(blueprint.size, blueprint.floors)
    ]

    return MinecraftPlan(
        title=blueprint.title,
        size=blueprint.size,
        materials=materials,
        floors=blueprint.floors,
        rooms=blueprint.rooms,
        summary=_compact_summary(blueprint, materials),
        ascii_plan=_ascii_plan(blueprint),
        notes=blueprint.notes,
    )