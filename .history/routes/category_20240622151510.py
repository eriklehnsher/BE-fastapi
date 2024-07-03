from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from pymongo.collection import Collection
from db import categories_collection
from models.category import CategoryInDB

router = APIRouter()


@router.post("/categories/", response_model=CategoryInDB)
async def create_category(category: CategoryInDB):
    category_dict = category.model_dump()
    result =  categories_collection.insert_one(category_dict)
    category.id = str(result.inserted_id)
    return category


@router.get("/categories/", response_model=List[CategoryInDB])
async def read_categories(skip: int = 0, limit: int = 10):
    categories = []
    cursor = categories_collection.find().skip(skip).limit(limit)
    async for category in cursor:
        category_model = CategoryInDB(**category)
        category_model.id = str(category_model.id)
        categories.append(category_model)
    return categories


@router.get("/categories/{category_id}", response_model=CategoryInDB)
async def read_category(category_id: str):
    category = await categories_collection.find_one({"_id": ObjectId(category_id)})
    if category:
        category_model = CategoryInDB(**category)
        category_model.id = str(category_model.id)
        return category_model
    raise HTTPException(status_code=404, detail="Category not found")


@router.put("/categories/{category_id}", response_model=CategoryInDB)
async def update_category(category_id: str, category: CategoryInDB):
    category_dict = category.model_dump(exclude_unset=True)
    if await categories_collection.find_one({"_id": ObjectId(category_id)}):
        await categories_collection.update_one(
            {"_id": ObjectId(category_id)}, {"$set": category_dict}
        )
        category.id = category_id
        return category
    raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/categories/{category_id}", response_model=dict)
async def delete_category(category_id: str):
    result = await categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Category deleted"}
    raise HTTPException(status_code=404, detail="Category not found")
