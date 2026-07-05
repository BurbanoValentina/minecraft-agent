# Minecraft Agent

Minecraft Agent es una interfaz experimental para planear construcciones con estética clara, tono de Overworld y referencias directas a Minecraft. La app combina FastAPI, una vista web ligera y un flujo con IA para generar ideas de casas, bases y estructuras con materiales coherentes.

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
- Groq API (LLM) para generación de planes.
- AWS Elastic Beanstalk (EC2 + CloudFormation) para despliegue.

## Estructura

```text
src/
  main.py
  agents/
    architect.py
    materials.py
    planner.py
  services/
    groq.py
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
3. El planificador consulta a Groq para generar el plano; si falla, usa una lógica local de respaldo.
4. Los agentes calculan el tamaño y los materiales.
5. La interfaz muestra el resultado en una tarjeta inspirada en Minecraft.

## Cómo ejecutar

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Necesitas una variable de entorno `GROQ_API_KEY` en un archivo `.env` (ver sección de variables más abajo).

## Endpoints

- `GET /` muestra la interfaz web.
- `GET /health` confirma que el servicio está arriba.
- `POST /api/build` genera el plan de construcción a partir del texto del usuario.

## Notas del proyecto

- La experiencia está pensada para verse bien con colores claros y un estilo limpio.
- El agente usa Groq (Llama 3.3) para generar el plano; si falla, cae a una lógica local determinista de respaldo.
- ngrok sigue siendo útil para compartir la app durante pruebas o demos locales.

## Despliegue en AWS

La app está desplegada en **Elastic Beanstalk** (single instance, EC2 t3.micro, dentro del free tier).

> **Nota:** el ambiente no se mantiene activo permanentemente. Se apaga cuando no hay una demo en curso, para evitar costos innecesarios.

### Levantar el ambiente

```bash
eb init -p python-3.12 minecraft-agent --region us-east-1
eb create minecraft-agent-env --instance-type t3.micro --single
eb setenv GROQ_API_KEY=tu_clave
eb deploy
```

### Apagar el ambiente

```bash
eb terminate minecraft-agent-env
```

### Variables de entorno requeridas

| Variable | Descripción |
|---|---|
| `GROQ_API_KEY` | Clave de la API de Groq ([console.groq.com/keys](https://console.groq.com/keys)) |

## Siguiente mejora sugerida

Ampliar el prompt del sistema en `planner.py` para soportar más estilos (castillos, aldeas, granjas) y agregar streaming de respuesta en el endpoint.
