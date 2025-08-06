from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


client = MongoClient(os.getenv("MONGO_URI"))
history_collection = client["chat_db"]["chat_history"]

def save_interaction(session_id, user_input, response):
    print("saving to db:", session_id, user_input, response)
    history_collection.insert_one({
        "request_id": str(uuid4()),
        "session_id": session_id,
        "timestamp": datetime.utcnow(),
        "user_input": user_input,
        "response": response
    })

def get_recent_history(session_id, limit=5):
    cursor = history_collection.find({"session_id": session_id}).sort("timestamp", -1).limit(limit)
    return list(reversed([
        {"user": e["user_input"], "agent": e["response"]}
        for e in cursor
    ]))
