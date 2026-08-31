from flask import Flask, jsonify, send_from_directory
import os

app = Flask(_name_)

@app.route('/')
def home():
    # This will now show your index.html landing page
    return send_from_directory('.', 'index.html')

@app.route('/api')
def api():
    # This will show your JSON
    return jsonify({
        "name": "First Meta",
        "version": "0.2.3 FINAL FIX",
        "builder": "Andrea Kisumu",
        "groq_key": bool(os.getenv("GROQ_API_KEY")),
        "status": "live"
    })

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
