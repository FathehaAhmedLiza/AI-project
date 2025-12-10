from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

app = Flask(__name__)

def ask_openrouter(message, system_prompt=None, model="openrouter/auto"):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7
    }

    resp = requests.post(API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    result = ask_openrouter(user_message, system_prompt="You are a helpful assistant.")
    reply = (
        result.get("choices", [{}])[0]
              .get("message", {})
              .get("content", "")
    )

    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("Server running → http://127.0.0.1:5000")
    app.run(debug=True)