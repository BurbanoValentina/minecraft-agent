from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.agents.planner import generate_plan

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Minecraft Agent", version="1.0.0")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "default_prompt": "Quiero una casa medieval para supervivencia.",
        },
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "minecraft-agent"}


@app.post("/api/build")
async def build_plan(user_request: str = Form(...)):
    plan = await generate_plan(user_request)
    return plan.model_dump()