from typing import List
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


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


class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    user_tags: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "username": "user123",
                "email": "user123@example.com",
                "hashed_password": "hashedpassword",
                "first_name": "John",
                "last_name": "Doe",
                "user_tags": ["coding", "photography"]
            }
        }
