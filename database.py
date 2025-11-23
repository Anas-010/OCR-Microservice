import os
from pymongo import MongoClient
from pymongo.collection import Collection

# Default to local mongo if not specified
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ocr_db")

class Database:
    client: MongoClient = None
    db = None

    def connect(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        print(f"Connected to MongoDB at {MONGO_URI}")

    def close(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

db = Database()
