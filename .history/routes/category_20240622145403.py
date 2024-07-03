from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from pymongo import MongoClient
from db import categories_collection
from models.category import Category

router = APIRouter()

# Kết nối tới MongoDB

@router.post("/categories/", response_model=Category)
async def create_category(category: Category):
    category_dict = category.dict(exclude_unset=True)
    inserted_result = categories_collection.insert_one(category_dict)
    category.id = inserted_result.inserted_id
    return category

@router.get("/categories/", response_model=List[Category])
async def get_categories():
    categories = []
    for category in categories_collection.find():
        categories.append(Category(**category))
    return categories

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    if category:
        return Category(**category)
    raise HTTPException(status_code=404, detail="Category not found")

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(category_id: str, category: Category):
    category_dict = category.dict(exclude_unset=True)
    if categories_collection.find_one({"_id": ObjectId(category_id)}):
        categories_collection.update_one({"_id": ObjectId(category_id)}, {"$set": category_dict})
        category.id = category_id
        return category
    raise HTTPException(status_code=404, detail="Category not found")

@router.delete("/categories/{category_id}", response_model=dict)
async def delete_category(category_id: str):
    result = categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Category deleted"}
    raise HTTPException(status_code=404, detail="Category not found")
