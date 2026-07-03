# Minecraft Agent

Minecraft Agent es una interfaz experimental para planear construcciones con estética clara, tono de Overworld y referencias directas a Minecraft. La app combina FastAPI, una vista web ligera y un flujo local para generar ideas de casas, bases y estructuras con materiales coherentes.

## Qué incluye

- Una API web con FastAPI para generar planes de construcción.
- Una interfaz clara con panel de estado, formulario y salida lista para copiar.
- Referencias visuales a bloques, biomas, redstone y supervivencia.
- Lógica separada en módulos para arquitecto, planificador y materiales.

## Stack

- Python 3.11+.
- FastAPI.
- Uvicorn.
- python-dotenv.

## Estructura

```text
src/
  main.py
  agents/
    architect.py
    materials.py
    planner.py
  prompts/
    architect_prompt.txt
  templates/
    index.html
  static/
    app.js
    styles.css
```

## Flujo

1. El usuario describe lo que quiere construir.
2. FastAPI recibe la petición en `src/main.py`.
3. Los agentes calculan el plan, el tamaño y los materiales.
4. La interfaz muestra el resultado en una tarjeta inspirada en Minecraft.

## Cómo ejecutar

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Endpoints

- `GET /` muestra la interfaz web.
- `GET /health` confirma que el servicio está arriba.
- `POST /api/build` genera el plan de construcción a partir del texto del usuario.

## Notas del proyecto

- La experiencia está pensada para verse bien con colores claros y un estilo limpio.
- ngrok sigue siendo útil para compartir la app durante pruebas o demos.
- La lógica local se mantiene determinista para que el resultado sea estable.

## Siguiente mejora sugerida

Conectar `main.py`, `planner.py` y `services/claude.py` para ampliar el agente con respuestas más ricas sobre castillos, aldeas, granjas y bases automáticas.
