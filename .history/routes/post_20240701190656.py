from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from pymongo import MongoClient
from db import xalothongtin_posts, kenhtao_posts
from models.post import PostInDB, PostModel
import datetime

router = APIRouter()


@router.post("/xalothongtin/posts/", response_model=PostInDB)
async def create_post(post: PostModel):
    post_dict = post.model_dump(exclude_unset=True)
    now = datetime.datetime.now()
    post_dict["created_at"] = now
    post_dict["updated_at"] = now
    inserted_result = xalothongtin_posts.insert_one(post_dict)
    post_dict["_id"] = str(inserted_result.inserted_id)
    return PostInDB(**post_dict)

import asyncio

@router.get("/posts/category/{category_name}", response_model=List[PostInDB])
async def get_posts_by_category_name(category_name: str):
    posts = []
    cursor = xalothongtin_posts.find({"categories_name": category_name})
    tasks = []
    async for document in cursor:
        tasks.append(asyncio.create_task(process_post(document, posts)))
    await asyncio.gather(*tasks)
    return posts

async def process_post(document, posts):
    post = PostInDB(**document)
    posts.append(post)



@router.get("/xalothongtin/posts/", response_model=List[PostInDB])
async def get_posts():
    posts = []
    for post in xalothongtin_posts.find():
        post["_id"] = str(post["_id"])
        posts.append(PostInDB(**post))
    return posts


@router.get("/xalothongtin/posts/{post_id}", response_model=PostInDB)
async def get_post(post_id: str):
    post = xalothongtin_posts.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])
        return PostInDB(**post)
    raise HTTPException(status_code=404, detail="Post not found")


@router.put("/xalothongtin/posts/{post_id}", response_model=PostInDB)
async def update_post(post_id: str, post: PostModel):
    post_dict = post.model_dump(exclude_unset=True)
    post_dict["updated_at"] = datetime.datetime.now()
    if xalothongtin_posts.find_one({"_id": ObjectId(post_id)}):
        xalothongtin_posts.update_one({"_id": ObjectId(post_id)}, {"$set": post_dict})
        post_dict["_id"] = post_id
        return PostInDB(**post_dict)
    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/xalothongtin/posts/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    result = xalothongtin_posts.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")


# endpoint - KENH-TAO


@router.post("/kenhtao/posts/", response_model=PostInDB)
async def create_post(post: PostModel):
    post_dict = post.model_dump(exclude_unset=True)
    now = datetime.datetime.now()
    post_dict["created_at"] = now
    post_dict["updated_at"] = now
    inserted_result = kenhtao_posts.insert_one(post_dict)
    post_dict["_id"] = str(inserted_result.inserted_id)
    return PostInDB(**post_dict)


@router.get("/kenhtao/posts/", response_model=List[PostInDB])
async def get_posts():
    posts = []
    for post in kenhtao_posts.find():
        post["_id"] = str(post["_id"])
        posts.append(PostInDB(**post))
    return posts


@router.get("/kenhtao/posts/{post_id}", response_model=PostInDB)
async def get_post(post_id: str):
    post = kenhtao_posts.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])
        return PostInDB(**post)
    raise HTTPException(status_code=404, detail="Post not found")


@router.put("/kenhtao/posts/{post_id}", response_model=PostInDB)
async def update_post(post_id: str, post: PostModel):
    post_dict = post.model_dump(exclude_unset=True)
    post_dict["updated_at"] = datetime.datetime.now()
    if kenhtao_posts.find_one({"_id": ObjectId(post_id)}):
        kenhtao_posts.update_one({"_id": ObjectId(post_id)}, {"$set": post_dict})
        post_dict["_id"] = post_id
        return PostInDB(**post_dict)
    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/kenhtao/posts/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    result = kenhtao_posts.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")
