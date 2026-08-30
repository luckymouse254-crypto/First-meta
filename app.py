import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# PASTE YOUR GROQ KEY HERE - keep the quotes
os.environ["GROQ_API_KEY"] = "gsk_YOUR_KEY_HERE"

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI(title="First Meta")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

memory = {}

@app.get("/")
def home():
    return {"app": "First Meta", "status": "Running - Built by Andrea"}

@app.post("/chat")
def chat(user_id: str = "andrea", message: str = "hello"):
    if user_id not in memory:
        memory[user_id] = [{"role": "system", "content": "You are First Meta, built by Andrea. Be helpful and remember context."}]
    memory[user_id].append({"role": "user", "content": message})
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=memory[user_id]
    )
    reply = res.choices[0].message.content
    memory[user_id].append({"role": "assistant", "content": reply})
    return {"reply": reply}