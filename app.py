from flask import Flask, render_template, request, jsonify
import os

app = Flask(_name_)

@app.route('/')
def home():
    return "First Meta is Live 🚀 Builder: Andrea Kisumu Version: 0.2.3 FINAL FIX"
