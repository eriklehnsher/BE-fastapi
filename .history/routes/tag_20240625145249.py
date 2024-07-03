from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bson import ObjectId
from pymongo.collection import Collection
from db import xalothongtin_tags, kenhtao_tags 
from models.tag import TagInDB

router = APIRouter()


@router.post("/xalothongtin/tags/", response_model=TagInDB)
async def create_tag(tag: TagInDB):
    tag_dict = tag.model_dump()
    result =  xalothongtin_tags.insert_one(tag_dict)
    tag.id = str(result.inserted_id)
    return tag


@router.get("/xalothongtin/tags/", response_model=List[TagInDB])
async def read_tags(skip: int = 0, limit: int = 10):
    tags = []
    cursor = xalothongtin_tags.find().skip(skip).limit(limit)
    async for tag in cursor:
        tag_model = TagInDB(**tag)
        tag_model.id = str(tag_model.id)  # Chuyển đổi ObjectId thành str
        tags.append(tag_model)
    return tags


@router.get("/xalothongtin/tags/{tag_id}", response_model=TagInDB)
async def read_tag(tag_id: str):
    tag = await xalothongtin_tags.find_one({"_id": ObjectId(tag_id)})
    if tag:
        tag_model = TagInDB(**tag)
        tag_model.id = str(tag_model.id)  # Chuyển đổi ObjectId thành str
        return tag_model
    raise HTTPException(status_code=404, detail="Tag not found")


@router.put("/xalothongtin/tags/{tag_id}", response_model=TagInDB)
async def update_tag(tag_id: str, tag: TagInDB):
    tag_dict = tag.model_dump(exclude_unset=True)
    if await xalothongtin_tags.find_one({"_id": ObjectId(tag_id)}):
        await xalothongtin_tags.update_one({"_id": ObjectId(tag_id)}, {"$set": tag_dict})
        tag.id = tag_id
        return tag
    raise HTTPException(status_code=404, detail="Tag not found")


@router.delete("/xalothongtin/tags/{tag_id}", response_model=dict)
async def delete_tag(tag_id: str):
    result = await xalothongtin_tags.delete_one({"_id": ObjectId(tag_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Tag deleted"}
    raise HTTPException(status_code=404, detail="Tag not found")


# kenhtao

@router.post("/kenhtao/tags/", response_model=TagInDB)
async def create_tag(tag: TagInDB):
    tag_dict = tag.model_dump()
    result =  kenhtao_tags.insert_one(tag_dict)
    tag.id = str(result.inserted_id)
    return tag


@router.get("/kenhtao/tags/", response_model=List[TagInDB])
async def read_tags(skip: int = 0, limit: int = 10):
    tags = []
    cursor = kenhtao_tags.find().skip(skip).limit(limit)
    async for tag in cursor:
        tag_model = TagInDB(**tag)
        tag_model.id = str(tag_model.id)  # Chuyển đổi ObjectId thành str
        tags.append(tag_model)
    return tags


@router.get("/kenhtao/tags/{tag_id}", response_model=TagInDB)
async def read_tag(tag_id: str):
    tag = await kenhtao_tags.find_one({"_id": ObjectId(tag_id)})
    if tag:
        tag_model = TagInDB(**tag)
        tag_model.id = str(tag_model.id)  # Chuyển đổi ObjectId thành str
        return tag_model
    raise HTTPException(status_code=404, detail="Tag not found")


@router.put("/kenhtao/tags/{tag_id}", response_model=TagInDB)
async def update_tag(tag_id: str, tag: TagInDB):
    tag_dict = tag.model_dump(exclude_unset=True)
    if await kenhtao_tags.find_one({"_id": ObjectId(tag_id)}):
        await kenhtao_tags.update_one({"_id": ObjectId(tag_id)}, {"$set": tag_dict})
        tag.id = tag_id
        return tag
    raise HTTPException(status_code=404, detail="Tag not found")


@router.delete("/kenhtao/tags/{tag_id}", response_model=dict)
async def delete_tag(tag_id: str):
    result = await kenhtao_tags.delete_one({"_id": ObjectId(tag_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Tag deleted"}
    raise HTTPException(status_code=404, detail="Tag not found")