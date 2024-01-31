from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Schema for creating a new blog


class BlogCreate(BaseModel):
    blog_name: str = Field(..., example="My First Blog")
    description: str = Field(..., example="This is my first blog post.")
    pages: int = Field(..., example=5)
    content: str = Field(..., example="Detailed blog content goes here...")
    tags: List[str] = Field(..., example=["Python", "Web Development"])
    language: str = Field(..., example="English")

# Schema for updating an existing blog


class BlogUpdate(BaseModel):
    blog_name: Optional[str] = Field(None, example="Updated Blog Title")
    description: Optional[str] = Field(None, example="Updated description.")
    pages: Optional[int] = Field(None, example=10)
    content: Optional[str] = Field(None, example="Updated blog content...")
    tags: Optional[List[str]] = Field(
        None, example=["Programming", "Tutorial"])
    language: Optional[str] = Field(None, example="Spanish")

# Schema for outputting blog data


class BlogPublic(BaseModel):
    id: str = Field(..., example="507f191e810c19729de860ea")
    blog_name: str = Field(..., example="My First Blog")
    description: str = Field(..., example="This is my first blog post.")
    pages: int = Field(..., example=5)
    content: str = Field(..., example="Detailed blog content goes here...")
    published: datetime
    updated_on: datetime
    tags: List[str] = Field(..., example=["Python", "Web Development"])
    language: str = Field(..., example="English")
    author: str = Field(..., example="507f1f77bcf86cd799439011")

    class Config:
        orm_mode = True


class DashboardResponse(BaseModel):
    blogs: BlogPublic
