import requests

# Replace this with your OpenRouter API key 
OPENROUTER_API_KEY = "YOUR_API_KEY"

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# ==============================
# Models
MAIN_MODEL = "openrouter/auto"
FALLBACK_MODEL = "openrouter/auto"

# ==============================
def ask_jarvis(user_input, model=MAIN_MODEL):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are Jarvis, an AI assistant. Speak in a calm, confident and professional tone. Be helpful, precise and a little witty. Always answer as a loyal assistant to your user."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        # fallback to openrouter/auto if main model fails
        if model != FALLBACK_MODEL:
            print(f"Main model failed, switching to fallback model: {FALLBACK_MODEL}")
            return ask_jarvis(user_input, model=FALLBACK_MODEL)
        return f"Jarvis could not respond due to an API error: {e}"

# ==============================
# Main Loop
print("Jarvis (Mistral 3.1 24B) online — type 'exit' to quit.\n")

while True:
    user_text = input("You: ").strip()
    if user_text.lower() in ["exit", "quit"]:
        print("Jarvis: Goodbye!")
        break
    if not user_text:
        continue

    reply = ask_jarvis(user_text)
    print("Jarvis:", reply)
