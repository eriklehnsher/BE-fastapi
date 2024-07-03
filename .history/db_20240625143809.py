from pymongo import MongoClient
from bson.objectid import ObjectId
from models.user import UserInDB

client = MongoClient("mongodb://localhost:27017/")
db = client["CMS-ARTICLES"]
Users_db = db["users"]
xalothongtin_posts = db["xalothongtin_posts"]
kenhtao_posts = db["kenhtao_posts"]
tags_collection = db["tags"]
xalothongtin_categories = db["xalothongtin_categories"]
kenhtao_categories = db["kenhtao_categories"]
kenhtao_posts = db["kenhtao_posts"]
xalothongtin_tags = db["xalothongtin_tags"]
kenhtao_tags = db["kenhtao_tags"]
