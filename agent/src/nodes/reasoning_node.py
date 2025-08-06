import requests
import os
from dotenv import load_dotenv
from utils.logger import log_with_request_id
from utils.memory import build_chat_memory_prompt
from utils.dbhistory import save_interaction

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")

def reasoning_node(state):
    user_msg = state["user_input"]
    session_id = state["session_id"]
    request_id = f"{session_id}_{len(state['history'])}"

    # 🔍 Compact system prompt
    system_prompt = (
        "If financial: tool_call:rag\n"
        "If online search: tool_call:tavily\n"
        "Else: reply."
    )

    #memory prompt
    memory_prompt = build_chat_memory_prompt(session_id, user_msg)
    
    # 🔧 Minimal structure and compact prompt
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\n{memory_prompt}"}
                ]
            }
        ]
    }

   ## headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}

    response = requests.post(GEMINI_URL, json=data)
    response.raise_for_status()
    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    log_with_request_id(request_id, f"Gemini reply: {reply}")
    print("🤖 Gemini Reasoning:", reply)

    save_interaction(session_id, user_msg, reply)
    # Track reasoning
    state["history"].append(f"Reasoning: {reply}")
    state["decision"] = reply
    state["user_input"] = user_msg

    if not reply.strip().startswith("tool_call:"):
        state["result"] = reply

    return state