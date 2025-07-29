from graph import app, ChatState

if __name__ == "__main__":
   initial_state = {
    "history": [],
    "user_input": "What are the latest AI news?",  # forces Tavily
    "result": ""
}
output = app.invoke(initial_state)
print("✅ Final result:", output["result"])


