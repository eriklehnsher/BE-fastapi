from pymongo import MongoClient
from bson.objectid import ObjectId
from models.user import UserInDB

client = MongoClient("mongodb://localhost:27017/")
db = client["CMS-ARTICLES"]
Users_db = db["users"]
Posts_db = db["posts"]
Categories_db = db["categories"]
Tag_db = db["tags"]

# def create_user(user: UserInDB):
#     user_dict = user.model_dump()
#     inserted_id = Users_db.insert_one(user_dict).inserted_id
#     return str(inserted_id)

# def get_user_by_email(email: str):
#     return Users_db.find_one({"email": email})

# def get_user_by_id(user_id: str):
#     return Users_db.find_one({"_id": ObjectId(user_id)})
