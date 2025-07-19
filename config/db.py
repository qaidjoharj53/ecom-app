from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "hrone")

client = MongoClient(MONGODB_URL)

def get_database():
    return client[DATABASE_NAME]
