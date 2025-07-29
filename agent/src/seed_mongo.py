from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 🔌 Load environment variables
load_dotenv()

# 📌 Get your MongoDB URI from .env
MONGO_URI = os.getenv("MONGO_URI")

# ✅ Connect to MongoDB Atlas
print("🔌 Connecting to MongoDB...")
client = MongoClient(MONGO_URI)
print("✅ Connected! Databases:", client.list_database_names())

# 📂 Select database and collection
db = client["financial_data"]
collection = db["netsol_reports"]

# 🗑️ (Optional) Clear existing data to start fresh
collection.delete_many({})

# 📥 Sample documents
sample_docs = [
    {
        "company": "Netsol",
        "year": 2024,
        "quarter": "Q1",
        "report": "Netsol revenue increased by 15% in Q1 2024. Net profit grew by 10%."
    },
    {
        "company": "Netsol",
        "year": 2024,
        "quarter": "Q2",
        "report": "Netsol saw a decline in operating margin but maintained stable revenue growth in Q2 2024."
    },
    {
        "company": "Netsol",
        "year": 2023,
        "quarter": "Q4",
        "report": "In Q4 2023, Netsol expanded into European markets and increased R&D spending."
    }
]

# 📌 Insert sample documents
result = collection.insert_many(sample_docs)
print(f"✅ Inserted {len(result.inserted_ids)} documents into MongoDB!")
