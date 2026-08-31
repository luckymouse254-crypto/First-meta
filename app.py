"""
First Meta v0.2.1 - FIXED + SMART with FREE Groq
Built by Andrea in Kisumu - Aug 31 2026
FIX: No more 500 error! Works even without key!

Install: pip install fastapi uvicorn httpx
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os

# Try import httpx, if not available use fallback
try:
    import httpx
    HAS_HTTPX = True
except:
    HAS_HTTPX = False
    print("httpx not installed, will use fallback")

app = FastAPI(title="First Meta", version="0.2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = "You are First Meta built by Andrea from Kisumu, Kenya. Be friendly, helpful like Meta AI."

@app.get("/")
def home():
    return {
        "name": "First Meta",
        "version": "0.2.1 SMART - FIXED",
        "builder": "Andrea Kisumu",
        "status": "online - no more 500 error!",
        "endpoints": ["/chat", "/docs"],
        "has_groq_key": bool(os.getenv("GROQ_API_KEY")),
        "has_httpx": HAS_HTTPX
    }

@app.get("/chat")
async def chat_get(message: str = Query("Hello"), user_id: str = Query("andrea")):
    return await do_chat(message, user_id)

@app.post("/chat")
async def chat_post(message: str = Query("Hello"), user_id: str = Query("andrea")):
    return await do_chat(message, user_id)

async def do_chat(user_msg: str, user_id: str):
    groq_key = os.getenv("GROQ_API_KEY")
    
    # If no key or no httpx, give helpful message (NOT 500 error)
    if not groq_key:
        return {
            "reply": f"Hi {user_id}! First Meta v0.2.1 is LIVE! 🚀 I need FREE brain key. Add GROQ_API_KEY in Render Environment. Get free at console.groq.com/keys . You said: '{user_msg}'. Once you add key, I'll be super smart like Meta AI! Built by Andrea in Kisumu.",
            "model": "First-Meta-fallback-no-key-yet",
            "status": "need_api_key"
        }
    
    if not HAS_HTTPX:
        return {
            "reply": f"Hi {user_id}! I have your key but missing httpx library. Add 'httpx' to requirements.txt on GitHub and redeploy. You said: {user_msg}",
            "model": "missing-httpx"
        }
    
    # Try Groq FREE API
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_msg}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 600
                }
            )
            if res.status_code != 200:
                return {"reply": f"Groq error {res.status_code}: {res.text[:200]}. Check your key is correct gsk_... format. You said: {user_msg}", "model": "groq-error"}
            
            data = res.json()
            answer = data["choices"][0]["message"]["content"]
            return {"reply": answer, "model": "groq-llama-3.1-8b-instant-free", "user_id": user_id, "builder": "Andrea"}
    except Exception as e:
        # NEVER return 500, always return helpful json
        return {
            "reply": f"Oops error: {str(e)[:200]}. You said: '{user_msg}'. First Meta is still learning! Try again. (Builder: Andrea Kisumu)",
            "model": "error-handled",
            "error": str(e)[:300]
        }

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.1", "groq_ready": bool(os.getenv("GROQ_API_KEY"))}
