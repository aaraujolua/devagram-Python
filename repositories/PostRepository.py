from decouple import config
import motor.motor_asyncio
from bson import ObjectId
from models.PostModel import PostCreateModel

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

post_collection = database.get_collection("post")


def show_post_data(post):
     return {
        "id": str(post["_id"]) if "id" in post else "",
        "user": post['user'] if "user" in post else "",
        "photo": post['icon'] if "photo" in post else "",
        "legend": post['legend'] if "legend" in post else "",
        "date": post['date'] if "date" in post else "",
        "likes": post['likes'] if "likes" in post else "",
        "comments": post['comments'] if "comments" in post else "",
    }
     

async def create_post(post: PostCreateModel) -> dict:
    created_user = await post_collection.insert_one(user.__dict__)
    
    new_post = await post_collection.find_one({"_id": created_user.inserted_id})
    
    return show_post_data(new_post)


async def list_posts():
    return post_collection.find()
    
    
async def find_post(id: str):
    post = await post_collection.find_one({"_id": ObjectId(id)})
    
    if post:
        return show_post_data(post)
    
    
async def delete_post(id: str):
    post = await post_collection.find_one({"_id": ObjectId(id)})
    
    if post:
        await post_collection.delete_one({"_id": ObjectId(id)})