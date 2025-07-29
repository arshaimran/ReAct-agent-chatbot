import requests

# 🔑 Put your Gemini API key here
GEMINI_API_KEY = "AIzaSyDRMVppp1J_46YWVSWumWZDpJg5NylMVZU"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key="
    + GEMINI_API_KEY
)

def reasoning_node(state):
    user_msg = state["user_input"]

    # 📝 System prompt telling Gemini how to reason
    system_prompt = (
        "You are a smart assistant.\n"
        "- If the user asks about company financial data, respond with: tool_call:rag\n"
        "- If the user asks about something you need to search online, respond with: tool_call:tavily\n"
        "- Otherwise, reply directly with the answer."
    )

    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_prompt}\nUser: {user_msg}"}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_URL, json=data)
    response.raise_for_status()
    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    print("🤖 Gemini Reasoning:", reply)

    # Keep reasoning in history
    state["history"].append(f"Reasoning: {reply}")

    # Decide what happens next
    state["decision"] = reply          # for routing (tool_call or not)
    state["user_input"] = user_msg     # preserve original query

    # ✅ NEW: If Gemini gave a direct answer (not a tool_call), set it as result
    if not reply.strip().startswith("tool_call:"):
        state["result"] = reply        # UI can now show this

    return state
