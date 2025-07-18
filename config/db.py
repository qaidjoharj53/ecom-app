from pymongo import MongoClient

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "hrone"

client = MongoClient(MONGODB_URL)

def get_database():
    print("Connecting to database...")
    return client[DATABASE_NAME]
