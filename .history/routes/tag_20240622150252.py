from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId

from db import tags_collection
from models.tag import TagInDB

router = APIRouter()


@router.post("/tags/", response_model=TagInDB)
async def create_tag(tag: TagInDB):
    tag_dict = tag.model_dump(exclude_unset=True)
    inserted_result = tags_collection.insert_one(tag_dict)
    tag.id = inserted_result.inserted_id
    return tag


@router.get("/tags/", response_model=List[TagInDB])
async def get_tags():
    tags = []
    for tag in tags_collection.find():
        tag["_id"] = str(tag["_id"])  # Chuyển ObjectId thành str
        tags.append(TagInDB(**tag))
    return tags


@router.get("/tags/{tag_id}", response_model=TagInDB)
async def get_tag(tag_id: str):
    tag = tags_collection.find_one({"_id": ObjectId(tag_id)})
    if tag:
        return TagInDB(**tag)
    raise HTTPException(status_code=404, detail="Tag not found")


@router.put("/tags/{tag_id}", response_model=TagInDB)
async def update_tag(tag_id: str, tag: TagInDB):
    tag_dict = tag.model_dump(exclude_unset=True)
    if tags_collection.find_one({"_id": ObjectId(tag_id)}):
        tags_collection.update_one({"_id": ObjectId(tag_id)}, {"$set": tag_dict})
        return {**tag.model_dump(), "id": tag_id}
    raise HTTPException(status_code=404, detail="Tag not found")


@router.delete("/tags/{tag_id}", response_model=dict)
async def delete_tag(tag_id: str):
    result = tags_collection.delete_one({"_id": ObjectId(tag_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Tag deleted"}
    raise HTTPException(status_code=404, detail="Tag not found")
