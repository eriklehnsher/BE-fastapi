from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
import datetime
from pymongo import MongoClient
from db import posts_collection, Users_db
from models.post import PostInDB, PostModel

router = APIRouter()

# Kết nối tới MongoDB


@router.post("/posts/", response_model=PostInDB)
async def create_post(post: PostModel):

    post_dict = post.model_dump(exclude_unset=True)
    post_dict["created_at"] = datetime.datetime.now().isoformat()
    post_dict["updated_at"] = datetime.datetime.now().isoformat()
    inserted_result = posts_collection.insert_one(post_dict)
    post.id = str(inserted_result.inserted_id)  # Chuyển ObjectId thành str
    return post


@router.get("/posts/", response_model=List[PostInDB])
async def get_posts():
    posts = []
    for post in posts_collection.find():
        post["_id"] = str(post["_id"])  # Chuyển ObjectId thành str
        posts.append(PostInDB(**post))
    return posts


@router.get("/posts/{post_id}", response_model=PostInDB)
async def get_post(post_id: str, post : PostInDB):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])  # Chuyển ObjectId thành str
        return PostInDB(**post)
    raise HTTPException(status_code=404, detail="Post not found")


@router.get("/posts/{post_id}/author", response_model=dict)
async def read_post_author(post_id: str):
    post =  posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        author_id = post.get("author_id")
        if author_id:
            user =  Users_db.find_one({"_id": ObjectId(author_id)})
            if user:
                return {
                    "id": str(user["_id"]),
                    "username": user["username"],
                    "email": user["email"],
                    "avatar": user.get("avatar", ""),
                    # Add other user information as needed
                }
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=404, detail="Author ID not found in post")
    raise HTTPException(status_code=404, detail="Post not found")


@router.put("/posts/{post_id}", response_model=PostInDB)
async def update_post(post_id: str, post: PostInDB):
    post_dict = post.model_dump(exclude_unset=True)
    if posts_collection.find_one({"_id": ObjectId(post_id)}):
        post_dict["updated_at"] = datetime.datetime.now().isoformat()
        posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_dict})
        post_dict["_id"] = post_id  # Giữ nguyên _id là str
        return post_dict
    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    result = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")
