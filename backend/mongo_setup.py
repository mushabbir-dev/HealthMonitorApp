from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file (used locally)
load_dotenv()

# Get the MongoDB URI from environment (Render or local .env)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

if not MONGO_URI:
    print("⚠️ Warning: MONGO_URI is not set. Check your environment variables.")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["HealthMonitorDB"]
collection = db["DeviceData"]

def save_encrypted_data(encrypted_string):
    try:
        collection.insert_one({
            "encrypted_data": encrypted_string
        })
        print("✅ Data saved to MongoDB.")
    except Exception as e:
        print("❌ MongoDB Save Error:", e)
