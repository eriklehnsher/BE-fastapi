from pymongo import MongoClient
from bson.objectid import ObjectId
from models.user import UserInDB

client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]
collection = db["users_db"]

def create_user(user: UserInDB):
    user_dict = user.dict()
    inserted_id = collection.insert_one(user_dict).inserted_id
    return str(inserted_id)

def get_user_by_email(email: str):
    return collection.find_one({"email": email})

def get_user_by_id(user_id: str):
    return collection.find_one({"_id": ObjectId(user_id)})
