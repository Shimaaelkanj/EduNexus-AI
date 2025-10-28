"""db_handler.py
Small MongoDB helper used by tests and the demo API.
The code assumes a local MongoDB instance for development.
"""
from pymongo import MongoClient
from datetime import datetime
import json
import os

# Default: local MongoDB. For Atlas, replace with your connection string.
client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
db = client["career_assistant_db"]
collection = db["cvs"]


def save_cv_analysis(filename, skills_found, skills_missing):
    """Insert an analysis document if it does not already exist for the filename."""
    if collection.find_one({"filename": filename}):
        # Already exists: do nothing
        return
    document = {
        "filename": filename,
        "skills_found": skills_found,
        "skills_missing": skills_missing,
        "created_at": datetime.now()
    }
    collection.insert_one(document)


def get_all_cvs():
    """Return a list of saved CV analysis documents (without Mongo _id)."""
    return list(collection.find({}, {"_id": 0}))


if __name__ == "__main__":
    filename = "cv_sample.pdf"
    skills_found = ["Python", "SQL"]
    skills_missing = ["Django", "Machine Learning"]
    save_cv_analysis(filename, skills_found, skills_missing)
    all_cvs = get_all_cvs()
    print(json.dumps(all_cvs, indent=2, ensure_ascii=False))
