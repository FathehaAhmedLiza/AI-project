# simple_chatbot.py
# Requirements: requests, python-dotenv
# Run: python simple_chatbot.py

import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise SystemExit("Set OPENROUTER_API_KEY in a .env file")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

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

    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()

def main():
    print("Simple OpenRouter chatbot — type 'exit' to quit.")
    system = "You are a helpful assistant."
    while True:
        user_in = input("You: ").strip()
        if user_in.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        try:
            result = ask_openrouter(user_in, system_prompt=system)
            assistant_msg = (
                result
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            print("Bot:", assistant_msg.strip())
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()