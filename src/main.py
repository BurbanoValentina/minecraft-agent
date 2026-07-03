from fastapi import FastAPI

app = FastAPI(title="Minecraft Agent")

@app.get("/")
def home():
    return {
        "message": "Minecraft AI Agent funcionando"
    }