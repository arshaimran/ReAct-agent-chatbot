from utils.dbhistory import get_recent_history

def build_chat_memory_prompt(session_id, user_input):
    history = get_recent_history(session_id)
    print("retrived history: ", history)
    if not history:
        return f"User: {user_input}\nAgent:"
    
    memory = "\n".join([f"User: {h['user']}\nAgent: {h['agent']}" for h in history])
    return f"{memory}\nUser: {user_input}\nAgent:"
