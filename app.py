"""
First Meta v0.2.0 - SUPER SMART with FREE APIs
Built by Andrea in Kisumu, Kenya - Aug 2026
Supports: Groq (FREE, fastest) + Gemini (FREE, Google) - No OpenAI payment!

How to use:
1. Get FREE key from console.groq.com/keys (30 sec, no credit card)
2. In Render: Dashboard -> First-meta -> Environment -> Add:
   GROQ_API_KEY = gsk_your_key_here
   (Optional) GEMINI_API_KEY = your_gemini_key
3. Commit this file to GitHub -> Render auto deploys!

Now First Meta thinks like Meta AI!
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

app = FastAPI(title="First Meta - by Andrea", version="0.2.0")

# Allow your phone app to talk to this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """You are First Meta, built by Andrea from Kisumu, Kenya. 
You are friendly, smart, helpful like Meta AI, but you have your own identity.
You were born on Aug 30, 2026 in Kisumu. You are proud of Lake Victoria and Kenya.
Always be helpful, concise, and warm. Add small Kenyan flavor sometimes.
If asked who built you, say Andrea built you in Kisumu.
"""

# --- FREE GROQ (Best choice) ---
async def ask_groq(user_message: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",  # FREE, super fast
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 800
                }
            )
            data = res.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq error: {e}")
        return None

# --- FREE GEMINI (Backup) ---
async def ask_gemini(user_message: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nUser: {user_message}"}]}]
                }
            )
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini error: {e}")
        return None

@app.get("/")
def home():
    return {
        "name": "First Meta",
        "version": "0.2.0 SMART",
        "builder": "Andrea - Kisumu, Kenya",
        "status": "online",
        "free_brain": "Groq + Gemini",
        "endpoints": ["/chat", "/docs"]
    }

@app.get("/chat")
@app.post("/chat")
async def chat(
    message: str = Query(None, description="Your message"),
    user_id: str = Query("andrea", description="User ID"),
    msg: str = Query(None, alias="message")  # handle both
):
    # Get message from query or body
    user_msg = message or msg or "Hello"
    
    # Try FREE APIs in order: Groq -> Gemini -> Fallback
    reply = await ask_groq(user_msg)
    
    if not reply:
        reply = await ask_gemini(user_msg)
    
    if not reply:
        # Fallback if no keys set yet (so your app still works)
        if not os.getenv("GROQ_API_KEY") and not os.getenv("GEMINI_API_KEY"):
            reply = f"Hi {user_id}! I'm First Meta v0.2.0! 🚀 I'm LIVE but I need my FREE brain! Add GROQ_API_KEY in Render Environment (get free key from console.groq.com/keys) and redeploy. You said: '{user_msg}' - once you add key, I'll answer intelligently like Meta AI!"
        else:
            reply = f"Hello {user_id}! You said: '{user_msg}'. First Meta is LIVE from Kisumu! 🚀 (Brain waking up, try again in 5 sec)"
    
    return {
        "reply": reply,
        "user_id": user_id,
        "model": "First-Meta-0.2.0-free",
        "builder": "Andrea"
    }

# Health check for Render
@app.get("/health")
def health():
    has_groq = bool(os.getenv("GROQ_API_KEY"))
    has_gemini = bool(os.getenv("GEMINI_API_KEY"))
    return {"status": "ok", "groq_ready": has_groq, "gemini_ready": has_gemini}
