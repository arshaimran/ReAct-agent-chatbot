import requests
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")

def reasoning_node(state):
    user_msg = state["user_input"]

    # 🔍 Compact system prompt
    system_prompt = (
        "If financial: tool_call:rag\n"
        "If online search: tool_call:tavily\n"
        "Else: reply."
    )

    # 🔧 Minimal structure and compact prompt
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\nQ: {user_msg}"}
                ]
            }
        ]
    }

   ## headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}

    response = requests.post(GEMINI_URL, json=data)
    response.raise_for_status()
    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    print("🤖 Gemini Reasoning:", reply)

    # Track reasoning
    state["history"].append(f"Reasoning: {reply}")
    state["decision"] = reply
    state["user_input"] = user_msg

    if not reply.strip().startswith("tool_call:"):
        state["result"] = reply

    return state
