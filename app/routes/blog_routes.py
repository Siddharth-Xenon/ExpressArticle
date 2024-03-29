from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from schemas import blog_schema, user_schema
from dependencies import database, auth
from datetime import datetime
import bson
from bson import ObjectId
from dependencies import auth
router = APIRouter()


@router.get("/dashboard", response_model=list[blog_schema.BlogPublic])
async def get_blogs(page: int = 1, page_size: int = 10, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    user_tags = database.get_user_tags(current_user["_id"])
    blogs = database.get_blogs_by_tags(user_tags, page, page_size)
    return [blog for blog in blogs]


@router.get("/", response_model=List[blog_schema.BlogPublic])
async def read_all_blogs(
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    page_size: int = Query(10, ge=1, description="Number of blogs per page")
):
    skip = (page - 1) * page_size
    return database.list_blogs(skip, page_size)


@router.post("/", response_model=blog_schema.BlogPublic)
async def create_blog(blog: blog_schema.BlogCreate, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    new_blog_data = blog.dict()
    print(new_blog_data)
    print(current_user)
    new_blog_data['author'] = current_user["_id"]
    current_time = bson.datetime.datetime.utcnow()
    new_blog_data['published'] = current_time
    new_blog_data['updated_on'] = current_time
    new_blog_id = database.create_blog(new_blog_data)
    if not new_blog_id:
        raise HTTPException(status_code=400, detail="Error creating blog")
    return {**new_blog_data, "id": new_blog_id}


@router.put("/{blog_id}", response_model=blog_schema.BlogPublic)
async def update_blog(blog_id: str, blog_update: blog_schema.BlogUpdate, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    update_result = database.update_blog(
        blog_id, blog_update.dict(exclude_unset=True))
    blog = database.get_blog(blog_id)
    if blog['author'] != current_user["_id"]:
        raise HTTPException(
            status_code=401, detail="Cannot access this blog as it belongs to other user.")
    if not update_result:
        raise HTTPException(
            status_code=404, detail="Blog not found or update failed")
    updated_blog = database.get_blog(blog_id)
    return updated_blog


@router.get("/{blog_id}", response_model=blog_schema.BlogPublic)
async def read_blog(blog_id: str):
    blog = database.get_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.delete("/{blog_id}", response_model=dict)
async def delete_blog(blog_id: str, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    blog = database.get_blog(blog_id)
    if current_user['_id'] != blog["author"]:
        raise HTTPException(
            status_code=401, detail="You are not the owner of this blog")
    delete_result = database.delete_blog(blog_id)
    if not delete_result:
        raise HTTPException(
            status_code=404, detail="Blog not found or delete failed")
    return {"message": "Blog successfully deleted"}
