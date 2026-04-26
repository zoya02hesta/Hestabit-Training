import requests

API_URL = "http://127.0.0.1:8000/chat"

while True:
    user_input = input("You: ")

    payload = {
        "system_prompt": "You are a helpful assistant",
        "user_prompt": user_input,
        "history": []
    }

    response = requests.post(API_URL, json=payload).json()

    print("Bot:", response["response"])