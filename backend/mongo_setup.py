from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file (used locally)
load_dotenv()

# Get MongoDB URI (from environment or fallback to localhost)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

if not MONGO_URI:
    print("❌ MONGO_URI is not set. Exiting.")
    sys.exit(1)

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client["HealthMonitorDB"]
    collection = db["DeviceData"]
    print("✅ Connected to MongoDB successfully.")
except Exception as conn_error:
    print("❌ MongoDB Connection Error:", conn_error)
    sys.exit(1)

def save_encrypted_data(encrypted_string):
    try:
        collection.insert_one({
            "encrypted_data": encrypted_string
        })
        print("✅ Data saved to MongoDB.")
    except Exception as e:
        print("❌ MongoDB Save Error:", e)
