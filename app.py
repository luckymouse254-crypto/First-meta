"""
First Meta v0.2.3 - ULTIMATE FIX Aug 31 2026
Using ONLY current valid Groq models!
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os, httpx

app = FastAPI(title="First Meta", version="0.2.3")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SYSTEM_PROMPT = "You are First Meta, built by Andrea from Kisumu, Kenya. Be friendly, helpful, proud Kenyan. Like Meta AI."

@app.get("/")
def home():
    return {"name":"First Meta","version":"0.2.3 FINAL FIX","builder":"Andrea Kisumu","groq_key": bool(os.getenv("GROQ_API_KEY"))}

@app.get("/chat")
@app.post("/chat")
async def chat(message: str = Query("Hello"), user_id: str = Query("andrea")):
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return {"reply": f"Hi {user_id}! Add GROQ_API_KEY in Render. Free at console.groq.com/keys . You said: {message}", "need_key": True}
    
    # ONLY models that are ALIVE today per Groq docs Aug 2026
    valid_models = [
        "llama-3.3-70b-versatile",
        "llama-3.3-70b-specdec",
        "llama-3.1-70b-versatile",
        "gemma2-9b-it",
        "openai/gpt-oss-120b"
    ]
    
    for mdl in valid_models:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json"},
                    json={
                        "model": mdl,
                        "messages":[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":message}],
                        "max_tokens":700,
                        "temperature":0.7
                    }
                )
                if r.status_code==200:
                    ans = r.json()["choices"][0]["message"]["content"]
                    return {"reply": ans, "model": mdl, "builder":"Andrea Kisumu", "version":"0.2.3"}
                else:
                    # if model not found, continue to next
                    txt = r.text
                    if "model_not_found" in txt or "decommissioned" in txt or "does not exist" in txt:
                        continue
                    else:
                        return {"reply": f"Groq said for {mdl}: {txt[:400]}", "model": mdl}
        except Exception as e:
            continue
    
    return {"reply": "All models failed - your Groq key might be invalid. Get new free key at console.groq.com/keys and replace GROQ_API_KEY in Render Environment, then Save. Then wait 2 min.", "error":"all_failed"}

@app.get("/health")
def health():
    return {"status":"ok","version":"0.2.3","groq": bool(os.getenv("GROQ_API_KEY"))}
