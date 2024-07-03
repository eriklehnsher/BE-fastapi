from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from db import posts_collection
from models.post import PostInDB

router = APIRouter()

# Kết nối tới MongoDB



@router.get("/posts/", response_model=List[PostInDB])
async def get_posts():
    posts = []
    for post in posts_collection.find():
        posts.append(PostInDB(**post))
    return posts


@router.get("/posts/{post_id}", response_model=PostInDB)
async def get_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        return PostInDB(**post)
    raise HTTPException(status_code=404, detail="Post not found")


@router.post("/posts/", response_model=PostInDB)
async def create_post(post: PostInDB):
    post_dict = post.model_dump_json(exclude_unset=True)
    post_dict["created_at"] = datetime.utcnow()
    post_dict["updated_at"] = datetime.utcnow()
    inserted_result = posts_collection.insert_one(post_dict)
    post.id = inserted_result.inserted_id
    return post


@router.put("/posts/{post_id}", response_model=PostInDB)
async def update_post(post_id: str, post: PostInDB):
    post_dict = post.model_dump(exclude_unset=True)
    if posts_collection.find_one({"_id": ObjectId(post_id)}):
        post_dict["updated_at"] = datetime.utcnow()
        posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_dict})
        return {**post.model_dump(), "id": post_id}
    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    result = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")
