# src/services/groq.py
import os, httpx

URL = "https://api.groq.com/openai/v1/chat/completions"

async def ask_groq(prompt: str, system: str, model="llama-3.3-70b-versatile", json_mode=False) -> str:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("Falta GROQ_API_KEY")
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(URL, json=payload, headers={"Authorization": f"Bearer {key}"})
        if r.status_code != 200:
            print("GROQ ERROR:", r.text)  # para ver el detalle exacto
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]