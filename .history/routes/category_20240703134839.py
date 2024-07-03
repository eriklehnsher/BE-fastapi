from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from pymongo.collection import Collection
from db import xalothongtin_categories, kenhtao_categories
from models.category import CategoryInDB, CategoryModel

router = APIRouter()


@router.post("/xalothongtin/categories/", response_model=CategoryInDB)
async def create_category(category: CategoryModel):
    category_dict = category.model_dump()
    result = xalothongtin_categories.insert_one(category_dict)
    category_in_db = CategoryInDB(**category_dict, id=str(result.inserted_id))
    return category_in_db


@router.get("/xalothongtin/categories/", response_model=List[CategoryInDB])
async def read_categories(skip: int = 0, limit: int = 10):
    cursor = xalothongtin_categories.find().skip(skip).limit(limit)
    categories = await cursor.to_list(length=limit)

    # Convert ObjectId to string for each category
    categories = [
        CategoryInDB(**category, id=str(category["_id"])) for category in categories
    ]

    return categories


@router.get("/xalothongtin/categories/{category_id}", response_model=CategoryInDB)
async def read_category(category_id: str):
    category = await xalothongtin_categories.find_one({"_id": ObjectId(category_id)})
    if category:
        category_model = CategoryInDB(**category)
        category_model.id = str(category_model.id)
        return category_model
    raise HTTPException(status_code=404, detail="Category not found")


@router.put("/xalothongtin/categories/{category_id}", response_model=CategoryInDB)
async def update_category(category_id: str, category: CategoryInDB):
    category_dict = category.model_dump(exclude_unset=True)
    if await xalothongtin_categories.find_one({"_id": ObjectId(category_id)}):
        await xalothongtin_categories.update_one(
            {"_id": ObjectId(category_id)}, {"$set": category_dict}
        )
        category.id = category_id
        return category
    raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/categories/{category_id}", response_model=dict)
async def delete_category(category_id: str):
    result = await xalothongtin_categories.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Category deleted"}
    raise HTTPException(status_code=404, detail="Category not found")


# kenh tao


@router.post("/kenhtao/categories/", response_model=CategoryInDB)
async def create_category(category: CategoryInDB):
    category_dict = category.model_dump()
    result = kenhtao_categories.insert_one(category_dict)
    category.id = str(result.inserted_id)
    return category


@router.get("/kenhtao/categories/", response_model=List[CategoryInDB])
async def read_categories(skip: int = 0, limit: int = 10):
    categories = []
    cursor = kenhtao_categories.find().skip(skip).limit(limit)
    async for category in cursor:
        category_model = CategoryInDB(**category)
        category_model.id = str(category_model.id)
        categories.append(category_model)
    return categories


@router.get("/kenhtao/categories/{category_id}", response_model=CategoryInDB)
async def read_category(category_id: str):
    category = await kenhtao_categories.find_one({"_id": ObjectId(category_id)})
    if category:
        category_model = CategoryInDB(**category)
        category_model.id = str(category_model.id)
        return category_model
    raise HTTPException(status_code=404, detail="Category not found")


@router.put("/kenhtao/categories/{category_id}", response_model=CategoryInDB)
async def update_category(category_id: str, category: CategoryInDB):
    category_dict = category.model_dump(exclude_unset=True)
    if await kenhtao_categories.find_one({"_id": ObjectId(category_id)}):
        await kenhtao_categories.update_one(
            {"_id": ObjectId(category_id)}, {"$set": category_dict}
        )
        category.id = category_id
        return category
    raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/kenhtao/categories/{category_id}", response_model=dict)
async def delete_category(category_id: str):
    result = await kenhtao_categories.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Category deleted"}
    raise HTTPException(status_code=404, detail="Category not found")
