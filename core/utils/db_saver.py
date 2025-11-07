from pymongo import MongoClient
from datetime import datetime

# Adjust your connection string
client = MongoClient("mongodb://localhost:27017/")
db = client["EduNexusAI"]

def save_summary_to_db(data: dict, collection="summaries"):
    try:
        data["created_at"] = datetime.utcnow()
        db[collection].insert_one(data)
        print("[DB] Summary saved successfully.")
    except Exception as e:
        print(f"[DB Error] {e}")