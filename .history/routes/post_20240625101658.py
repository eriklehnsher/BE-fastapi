from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from pymongo import MongoClient
from db import posts_collection
from models.post import PostInDB, PostModel
import datetime

router = APIRouter()


@router.post("/posts/", response_model=PostInDB)
async def create_post(post: PostModel):
    post_dict = post.model_dump(exclude_unset=True)
    now = datetime.datetime.now()
    post_dict["created_at"] = now
    post_dict["updated_at"] = now
    inserted_result = posts_collection.insert_one(post_dict)
    post_dict["_id"] = str(inserted_result.inserted_id)
    return PostInDB(**post_dict)


@router.get("/posts/", response_model=List[PostInDB])
async def get_posts():
    posts = []
    for post in posts_collection.find():
        post["_id"] = str(post["_id"])
        posts.append(PostInDB(**post))
    return posts


@router.get("/posts/{post_id}", response_model=PostInDB)
async def get_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])
        return PostInDB(**post)
    raise HTTPException(status_code=404, detail="Post not found")


@router.put("/posts/{post_id}", response_model=PostInDB)
async def update_post(post_id: str, post: PostModel):
    post_dict = post.model_dump(exclude_unset=True)
    post_dict["updated_at"] = datetime.datetime.now()
    if posts_collection.find_one({"_id": ObjectId(post_id)}):
        posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_dict})
        post_dict["_id"] = post_id
        return PostInDB(**post_dict)
    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    result = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")
