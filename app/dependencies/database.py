from pymongo import MongoClient, errors
from bson import ObjectId, json_util
from datetime import datetime
import bson
from bson import ObjectId, datetime as bson_datetime
from utils.common_utils import calculate_relevance
from os import environ as env

# MongoDB configuration (You should replace these with your configuration)
# client = MongoClient(f"mongodb+srv://sidsolanki920:8493@blogapi.gyqcnws.mongodb.net/")
client = MongoClient(f"mongodb+srv://{env['MONGO_USER']}:{env['MONGO_PASS']}@blogapi.gyqcnws.mongodb.net/")
db = client["blogAPI"]

# print("updated")
def create_user(user_data):
    try:
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)
    except errors.PyMongoError as e:
        print(f"Error creating user: {e}")
        return None


def get_user_by_id(user_id: str):
    try:
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
        updated = False
        if update_data:
            result = db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": update_data})
            updated = result.modified_count > 0

        return updated
    except errors.PyMongoError as e:
        print(f"Error updating user: {e}")
        return False


def update_tags(user_id, update_data):
    tags_to_add = update_data.pop('add_tags', [])
    tags_to_remove = update_data.pop('remove_tags', [])

    try:
        if tags_to_add:
            result = db.users.update_one({"_id": ObjectId(user_id)}, {
                "$addToSet": {"user_tags": {"$each": tags_to_add}}})

        if tags_to_remove:
            result = db.users.update_one({"_id": ObjectId(user_id)}, {
                "$pullAll": {"user_tags": tags_to_remove}})
        result = db.users.find_one({"_id": ObjectId(user_id)})
        return result
    except errors.PyMongoError as e:
        print(f"Error updating user: {e}")
        return False


def get_user_id(email_or_username):
    try:
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
            result["id"] = str(result["_id"])
            return result
        return None
    except errors.PyMongoError as e:
        print(f"Error retrieving blog: {e}")
        return None


def update_blog(blog_id, update_data):
    try:
        update_data["updated_on"] = bson.datetime.datetime.utcnow()
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


def list_blogs(skip: int, limit: int):
    try:
        blogs = db.blogs.find().skip(skip).limit(limit)
        return [{"id": str(blog["_id"]), **blog} for blog in blogs]
    except errors.PyMongoError as e:
        print(f"Error listing blogs: {e}")
        return []


def get_user_tags(user_id):
    # Fetch user's followed tags from the database
    # Return a list of tags
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        return user["user_tags"]
    except errors.PyMongoError as e:
        print(f"Error while getting user tags: {e}")


def get_blogs_by_tags(tags, page, limit):
    blogs = db["blogs"]

    # Aggregation pipeline
    pipeline = [
        {
            # Fetch documents with similar tags
            '$match': {'tags': {'$in': tags}}
        },
        {
            # field that contains the intersection size
            '$project': {
                'blog': '$$ROOT',
                'intersectionSize': {
                    '$size': {
                        '$setIntersection': ['$tags', tags]
                    }
                }
            }
        },
        {
            # Sort by the size of the intersection
            '$sort': {'intersectionSize': -1}
        },
        {
            # Pagination
            '$skip': (page - 1) * limit
        },
        {
            '$limit': limit
        }
    ]

    result = blogs.aggregate(pipeline)

    paginated_blogs = [
        {'id': str(blog['blog']['_id']), **blog['blog']} for blog in result]
    # print(paginated_blogs)
    return paginated_blogs


