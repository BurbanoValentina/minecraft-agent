# src/agents/planner.py
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from src.agents.architect import HouseBlueprint
from src.agents.materials import estimate_medieval_materials
from src.services.groq import ask_groq

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "architect_prompt.txt"

SYSTEM_PROMPT = (
    "Eres un arquitecto experto en Minecraft. Responde ÚNICAMENTE con un JSON "
    "válido con estas claves: title (str), style (str), size (str, ej '12x12'), "
    "floors (int), rooms (list[str]), notes (list[str]). No agregues texto fuera del JSON."
)


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
            title="Casa Medieval", style="medieval", size="15x15", floors=2,
            rooms=["Sala", "Dormitorio", "Almacén", "Encantamientos"],
            notes=["Ideal para supervivencia", "Incluye techo alto y torres pequeñas"],
        )
    if "casa" in text:
        return HouseBlueprint(
            title="Casa de Supervivencia", style="survival", size="12x12", floors=1,
            rooms=["Sala", "Dormitorio", "Almacén"],
            notes=["Diseño compacto para empezar rápido"],
        )
    return HouseBlueprint(
        title="Refugio Base", style="general", size="10x10", floors=1,
        rooms=["Sala", "Almacén"], notes=["Base simple y funcional"],
    )


async def _get_blueprint(user_request: str) -> HouseBlueprint:
    try:
        raw = await ask_groq(user_request, SYSTEM_PROMPT, json_mode=True)
        data = json.loads(raw)
        return HouseBlueprint(**data)
    except Exception as e:
        print(f"[groq fallback] {e}")
        return _fallback_blueprint(user_request)


def _compact_summary(blueprint: HouseBlueprint, materials: list[dict[str, int | str]]) -> str:
    materials_text = "\n".join(f"- {item['quantity']} {item['name']}" for item in materials)
    rooms_text = ", ".join(blueprint.rooms)
    notes_text = "\n".join(f"- {note}" for note in blueprint.notes) if blueprint.notes else "- Sin notas"
    return (
        f"{blueprint.title}\nTamaño: {blueprint.size}\nPisos: {blueprint.floors}\n"
        f"Habitaciones: {rooms_text}\nMateriales:\n{materials_text}\nNotas:\n{notes_text}"
    )


def _ascii_plan(blueprint: HouseBlueprint) -> str:
    width = 15 if blueprint.size == "15x15" else 12 if blueprint.size == "12x12" else 10
    border = "+" + "-" * width + "+"
    middle = "|" + "Casa".center(width) + "|"
    return "\n".join([border, middle, border])


async def generate_plan(user_request: str) -> MinecraftPlan:
    blueprint = await _get_blueprint(user_request)
    materials = [
        {"name": m.name, "quantity": m.quantity}
        for m in estimate_medieval_materials(blueprint.size, blueprint.floors)
    ]
    return MinecraftPlan(
        title=blueprint.title, size=blueprint.size, materials=materials,
        floors=blueprint.floors, rooms=blueprint.rooms,
        summary=_compact_summary(blueprint, materials),
        ascii_plan=_ascii_plan(blueprint), notes=blueprint.notes,
    )
