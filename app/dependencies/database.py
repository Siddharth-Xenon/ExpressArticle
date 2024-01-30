from pymongo import MongoClient, errors
from bson import ObjectId, json_util
from datetime import datetime
from bson import ObjectId, datetime as bson_datetime

# MongoDB configuration (You should replace these with your configuration)
client = MongoClient(
    "mongodb+srv://sidsolanki920:8493@blogapi.gyqcnws.mongodb.net/")
db = client["blogAPI"]


def create_user(user_data):
    try:
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)
    except errors.PyMongoError as e:
        print(f"Error creating user: {e}")
        return None


def get_user_by_id(user_id: str):
    try:
        # Convert user_id to ObjectId for querying MongoDB
        result = db.users.find_one({"_id": ObjectId(user_id)})
        if result:
            # Convert ObjectId back to string for JSON serialization
            result["_id"] = str(result["_id"])
            return result
        return None
    except errors.PyMongoError as e:
        print(f"Error retrieving user by ID: {e}")
        return None


def update_user(user_id, update_data):

    try:
        # Separate the tag updates from other user data
        tags_to_add = update_data.pop('add_tags', [])
        tags_to_remove = update_data.pop('remove_tags', [])

        updated = False

        # Update general user details
        if update_data:
            result = db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": update_data})
            updated = result.modified_count > 0

        # Add tags to the user's tag list
        if tags_to_add:
            result = db.users.update_one({"_id": ObjectId(user_id)}, {
                                         "$addToSet": {"user_tags": {"$each": tags_to_add}}})
            updated = updated or result.modified_count > 0

        # Remove tags from the user's tag list
        if tags_to_remove:
            result = db.users.update_one({"_id": ObjectId(user_id)}, {
                                         "$pullAll": {"user_tags": tags_to_remove}})
            updated = updated or result.modified_count > 0

        return updated
    except errors.PyMongoError as e:
        print(f"Error updating user: {e}")
        return False


def get_user_id(email_or_username):
    try:
        # Query to find a user by username or email
        user = db.users.find_one(
            {"$or": [{"username": email_or_username}, {"email": email_or_username}]})
        if user:
            return str(user["_id"])
        else:
            return None
    except errors.PyMongoError as e:
        print(f"Error retrieving user ID: {e}")
        return None


def create_blog(blog_data):
    try:
        result = db.blogs.insert_one(blog_data)
        return str(result.inserted_id)
    except errors.PyMongoError as e:
        print(f"Error creating blog: {e}")
        return None


def get_blog(blog_id):
    try:
        result = db.blogs.find_one({"_id": ObjectId(blog_id)})
        if result:
            result["_id"] = str(result["_id"])
            return result
        return None
    except errors.PyMongoError as e:
        print(f"Error retrieving blog: {e}")
        return None


def update_blog(blog_id, update_data):
    try:
        result = db.blogs.update_one(
            {"_id": ObjectId(blog_id)}, {"$set": update_data})
        return result.modified_count > 0
    except errors.PyMongoError as e:
        print(f"Error updating blog: {e}")
        return False


def delete_blog(blog_id):
    try:
        result = db.blogs.delete_one({"_id": ObjectId(blog_id)})
        return result.deleted_count > 0
    except errors.PyMongoError as e:
        print(f"Error deleting blog: {e}")
        return False


def list_blogs():
    try:
        blogs = db.blogs.find()
        return [{"_id": str(blog["_id"]), **blog} for blog in blogs]
    except errors.PyMongoError as e:
        print(f"Error listing blogs: {e}")
        return []


blog_data = {
    "blog_name": "updating FastAPI",
    "description": "A comprehensive guide to FastAPI",
    "pages": 120,
    "content": "Content of the blog...",
    "published": bson_datetime.datetime(2021, 1, 1),
    "updated_on": bson_datetime.datetime(2021, 1, 2),
    "tags": ["Python", "Web Development"],
    "language": "English",
    "author": ObjectId('507f191e810c19729de860ea')
}

# print(delete_blog("65b807f9a07c322614d74a37"))

user_data = {
    "username": "user123",
    "first_name": "Sid",
    "add_tags": ["nature"],
    "remove_tags": ["coding"]
}


print(update_user(get_user_id("user123"), user_data))
