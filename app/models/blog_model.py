from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class PyObjectId(ObjectId):
    """
    Pydantic requires a custom validator for ObjectId type fields.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    # @classmethod
    # def __modify_schema__(cls, field_schema):
    #     field_schema.update(type='string')
    def __get_pydantic_json_schema__(cls, schema):
        schema['properties'][cls.__name__]['type'] = 'string'
        return schema


class BlogSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    blog_name: str = Field(...)
    description: str = Field(...)
    pages: int = Field(...)
    content: str = Field(...)
    published: datetime = Field(...)
    updated_on: datetime = Field(...)
    tags: List[str] = Field(...)
    language: str = Field(...)
    author: PyObjectId = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "blog_name": "Learning FastAPI",
                "description": "A comprehensive guide to FastAPI",
                "pages": 120,
                "content": "Content of the blog...",
                "published": "2021-01-01T00:00:00",
                "updated_on": "2021-01-02T00:00:00",
                "tags": ["Python", "Web Development"],
                "language": "English",
                "author": "ObjectId('507f191e810c19729de860ea')"
            }
        }
