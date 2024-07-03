from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bson import ObjectId
from pymongo.collection import Collection
from db import tags_collection
from models.tag import TagInDB

router = APIRouter()


@router.post("/tags/", response_model=TagInDB)
async def create_tag(tag: TagInDB):
    tag_dict = tag.model_dump()
    result =  tags_collection.insert_one(tag_dict)
    tag.id = str(result.inserted_id)
    return tag


@router.get("/tags/", response_model=List[TagInDB])
async def read_tags(skip: int = 0, limit: int = 10):
    tags = []
    cursor = tags_collection.find().skip(skip).limit(limit)
    async for tag in cursor:
        tag_model = TagInDB(**tag)
        tag_model.id = str(tag_model.id)  # Chuyển đổi ObjectId thành str
        tags.append(tag_model)
    return tags


@router.get("/tags/{tag_id}", response_model=TagInDB)
async def read_tag(tag_id: str):
    tag = await tags_collection.find_one({"_id": ObjectId(tag_id)})
    if tag:
        tag_model = TagInDB(**tag)
        tag_model.id = str(tag_model.id)  # Chuyển đổi ObjectId thành str
        return tag_model
    raise HTTPException(status_code=404, detail="Tag not found")


@router.put("/tags/{tag_id}", response_model=TagInDB)
async def update_tag(tag_id: str, tag: TagInDB):
    tag_dict = tag.model_dump(exclude_unset=True)
    if await tags_collection.find_one({"_id": ObjectId(tag_id)}):
        await tags_collection.update_one({"_id": ObjectId(tag_id)}, {"$set": tag_dict})
        tag.id = tag_id
        return tag
    raise HTTPException(status_code=404, detail="Tag not found")


@router.delete("/tags/{tag_id}", response_model=dict)
async def delete_tag(tag_id: str):
    result = await tags_collection.delete_one({"_id": ObjectId(tag_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Tag deleted"}
    raise HTTPException(status_code=404, detail="Tag not found")
