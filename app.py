"""
First Meta v0.2.2 - FIXED MODEL NAME
Groq changed model names - use new one!
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os, httpx

app = FastAPI(title="First Meta", version="0.2.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = "You are First Meta built by Andrea from Kisumu, Kenya. Be friendly, helpful, smart like Meta AI. Proud of Kenya."

@app.get("/")
def home():
    return {
        "name": "First Meta",
        "version": "0.2.2 SMART - MODEL FIXED",
        "builder": "Andrea Kisumu",
        "status": "online",
        "groq_key_set": bool(os.getenv("GROQ_API_KEY")),
        "model": "llama-3.3-70b-versatile (free, latest)"
    }

@app.get("/chat")
@app.post("/chat")
async def chat(message: str = Query("Hello"), user_id: str = Query("andrea")):
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not groq_key:
        return {
            "reply": f"Hi {user_id}! First Meta v0.2.2 is LIVE! I see you didn't add GROQ_API_KEY yet. Add it in Render -> Environment. Get FREE key at console.groq.com/keys . You said: '{message}'",
            "status": "need_api_key"
        }
    
    # Try latest Groq models (free) - in order
    models_to_try = [
        "llama-3.3-70b-versatile",  # NEWEST, best free
        "llama3-8b-8192",           # Old reliable free
        "mixtral-8x7b-32768"        # Backup
    ]
    
    for model_name in models_to_try:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                res = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                    json={
                        "model": model_name,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 700
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    answer = data["choices"][0]["message"]["content"]
                    return {"reply": answer, "model": model_name, "user_id": user_id, "builder": "Andrea Kisumu"}
                # if model not found, try next model
                if "model_not_found" in res.text or "does not exist" in res.text:
                    continue
                else:
                    return {"reply": f"Groq error with {model_name}: {res.text[:300]}", "model": model_name}
        except Exception as e:
            continue
    
    return {"reply": f"All Groq models failed. Check your key gsk_... is valid. Error: {str(e)[:200]}. You said: {message}", "status": "all_models_failed"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.2", "groq_ready": bool(os.getenv("GROQ_API_KEY"))}
