from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas import blog_schema, user_schema
from dependencies import database, auth

router = APIRouter()


@router.post("/", response_model=blog_schema.BlogPublic)
async def create_blog(blog: blog_schema.BlogCreate, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    new_blog_data = blog.dict()
    print(new_blog_data)
    new_blog_data['author'] = current_user.id
    new_blog_id = database.create_blog(new_blog_data)
    if not new_blog_id:
        raise HTTPException(status_code=400, detail="Error creating blog")
    return {**new_blog_data, "id": new_blog_id}


@router.get("/{blog_id}", response_model=blog_schema.BlogPublic)
async def read_blog(blog_id: str):
    blog = database.get_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.get("/", response_model=List[blog_schema.BlogPublic])
async def read_all_blogs():
    return database.list_blogs()


@router.put("/{blog_id}", response_model=blog_schema.BlogPublic)
async def update_blog(blog_id: str, blog_update: blog_schema.BlogUpdate, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    update_result = database.update_blog(
        blog_id, blog_update.dict(exclude_unset=True))
    if not update_result:
        raise HTTPException(
            status_code=404, detail="Blog not found or update failed")
    updated_blog = database.get_blog(blog_id)
    return updated_blog


@router.delete("/{blog_id}", response_model=dict)
async def delete_blog(blog_id: str, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    delete_result = database.delete_blog(blog_id)
    if not delete_result:
        raise HTTPException(
            status_code=404, detail="Blog not found or delete failed")
    return {"message": "Blog successfully deleted"}
