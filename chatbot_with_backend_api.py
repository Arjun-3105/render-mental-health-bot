from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

app = FastAPI()

class ChatRequest(BaseModel):
    user_message: str

# crisis
CRISIS_KEYWORDS = ["suicide", "kill myself", "cutting", "self-harm", "end it all"]

def detect_crisis(text):
    return any(word in text.lower() for word in CRISIS_KEYWORDS)

@app.post("/chat")
async def chat(data: ChatRequest):
    user_message = data.user_message

    # Crisis detection
    if detect_crisis(user_message):
        return {
            "response": "I'm really sorry you're feeling this way. You're not alone. Please consider calling a crisis line like 988 (in the U.S.) or reaching out to a trusted friend or therapist."
        }

    # LLM model
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "messages": [
            {"role": "system", "content": "You are a compassionate and supportive mental health assistant. You help users talk through their feelings in a non-judgmental, gentle, and helpful way."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return {"response": reply}
    else:
        return {"response": "Sorry, I'm having trouble responding right now."}
