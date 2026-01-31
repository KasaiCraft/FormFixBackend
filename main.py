from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow your Flutter app to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing, later set to your app domain
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.post("/analyze-form")
async def analyze_form(file: UploadFile = None, text: str = Form(None)):
    # Get form content
    if file:
        content = (await file.read()).decode("utf-8")  # text file only for now
    elif text:
        content = text
    else:
        return {"error": "No input provided"}

    # Call OpenRouter AI with MoonshotAI: Kimi K2 0711 model
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    payload = {
        "model": "MoonshotAI:Kimi K2 0711",  # <-- updated model
        "messages": [
            {"role": "system", "content": "You are a form analysis AI. Detect mistakes and provide solutions."},
            {"role": "user", "content": content}
        ]
    }
    response = requests.post("https://api.openrouter.ai/v1/chat/completions", json=payload, headers=headers)
    result = response.json()
    
    ai_output = result["choices"][0]["message"]["content"]
    return {"analysis": ai_output}
