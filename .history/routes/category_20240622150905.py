from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from pymongo import MongoClient
from db import categories_collection
from models.category import CategoryInDB

router = APIRouter()

# Kết nối tới MongoDB


@router.post("/categories/", response_model=CategoryInDB)
async def create_category(category: CategoryInDB):
    category_dict = category.model_dump(exclude_unset=True)
    inserted_result = categories_collection.insert_one(category_dict)
    category.id = inserted_result.inserted_id
    return category


@router.get("/categories/", response_model=List[CategoryInDB])
async def get_categories():
    categories = []
    for category in categories_collection.find():
        category["_id"] = str(category["_id"])  # Chuyển ObjectId thành str
        categories.append(CategoryInDB(**category))
    return categories


@router.get("/categories/{category_id}", response_model=CategoryInDB)
async def get_category(category_id: str):
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    if category:
        category["_id"] = str(category["_id"])
        return CategoryInDB(**category)
    raise HTTPException(status_code=404, detail="Category not found")


@router.put("/categories/{category_id}", response_model=CategoryInDB)
async def update_category(category_id: str, category: CategoryInDB):
    category_dict = category.model_dump(exclude_unset=True)
    if categories_collection.find_one({"_id": ObjectId(category_id)}):
        categories_collection.update_one(
            {"_id": ObjectId(category_id)}, {"$set": category_dict}
        )
        category.id = category_id
        return category
    raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/categories/{category_id}", response_model=dict)
async def delete_category(category_id: str):
    result = categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Category deleted"}
    raise HTTPException(status_code=404, detail="Category not found")
