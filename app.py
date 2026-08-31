from flask import Flask, jsonify
import os

app = Flask(_name_)

@app.route('/')
def home():
    return """
    <html>
    <head><title>First Meta</title>
    <style>
      body{background:#0a0a0a;color:white;font-family:sans-serif;text-align:center;padding:80px 20px}
      h1{font-size:42px} a{color:#00ff88;text-decoration:none;border:1px solid #00ff88;padding:12px 24px;border-radius:8px;display:inline-block;margin-top:20px}
    </style>
    </head>
    <body>
      <h1>First Meta is Live 🚀</h1>
      <p>Builder: Andrea Kisumu</p>
      <p>Version: 0.2.3 FINAL FIX</p>
      <p>Status: Live in Kisumu</p>
      <a href="/api">View API JSON</a>
    </body>
    </html>
    """

@app.route('/api')
def api():
    return jsonify({
        "name": "First Meta",
        "version": "0.2.3 FINAL FIX",
        "builder": "Andrea Kisumu",
        "groq_key": bool(os.getenv("GROQ_API_KEY")),
        "status": "live",
        "location": "Kisumu, KE"
    })

# Vercel needs this
# app variable is exported automatically
