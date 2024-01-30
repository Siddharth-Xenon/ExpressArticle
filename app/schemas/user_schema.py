from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# Schema for user registration


class Token(BaseModel):
    access_token: str = Field(..., example="your_token_here")
    token_type: str = Field(..., example="bearer")


class UserCreate(BaseModel):
    username: str = Field(..., example="user123")
    email: EmailStr = Field(..., example="user123@example.com")
    password: str = Field(..., example="strongpassword")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    user_tags: Optional[List[str]] = Field(
        [], example=["coding", "photography"])

# Schema for user login


class UserLogin(BaseModel):
    username: str = Field(..., example="user123")
    password: str = Field(..., example="strongpassword")

# Schema for updating user profile


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    user_tags: Optional[List[str]] = Field(
        None, example=["coding", "photography"])

# Schema for public user profile


class UserPublic(BaseModel):
    id: str = Field(..., example="507f191e810c19729de860ea")
    username: str = Field(..., example="user123")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    user_tags: List[str] = Field(..., example=["coding", "photography"])

    class Config:
        orm_mode = True
