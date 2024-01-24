from decouple import config
import motor.motor_asyncio
from bson import ObjectId
from models.PostModel import PostCreateModel
from utils.ConverterUtil import ConverterUtil

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

post_collection = database.get_collection("post")

converterUtil = ConverterUtil()


class PostRepository:
    
    async def create_post(self, post: PostCreateModel) -> dict:
        created_user = await post_collection.insert_one(post.__dict__)
        
        new_post = await post_collection.find_one({"_id": created_user.inserted_id})
        
        return converterUtil.post_converter(new_post)


    async def list_posts(self):
        return post_collection.find()
        
        
    async def find_post(self, id: str):
        post = await post_collection.find_one({"_id": ObjectId(id)})
        
        if post:
            return converterUtil.post_converter(post)
        
        
    async def delete_post(self, id: str):
        post = await post_collection.find_one({"_id": ObjectId(id)})
        
        if post:
            await post_collection.delete_one({"_id": ObjectId(id)})