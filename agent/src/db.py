# src/db.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # loads MONGO_URI from .env

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["financial_data"]
collection = db["netsol_reports"]

