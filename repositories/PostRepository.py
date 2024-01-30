from decouple import config
import motor.motor_asyncio
from bson import ObjectId
from models.PostModel import PostCreateModel
from utils.ConverterUtil import ConverterUtil
from datetime import datetime
from typing import List

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

post_collection = database.get_collection("post")

converterUtil = ConverterUtil()


class PostRepository:
    
    async def create_post(self, post: PostCreateModel, user_id) -> PostCreateModel:
        post_dict = {
            "user_id": ObjectId(user_id),
            "legend": post.legend,
            "likes": 0,
            "comments": [],
            "date": datetime.now()
        }
        
        created_post = await post_collection.insert_one(post_dict)
        
        new_post = await post_collection.find_one({"_id": created_post.inserted_id})
        
        return converterUtil.post_converter(new_post)
    
    
    async def update_post(self, id: str, post_data: dict):
        post = await post_collection.find_one({"_id": ObjectId(id)})
        
        if post:
            await post_collection.update_one({"_id": ObjectId(id)}, {"$set": post_data})
            
            updated_post = await post_collection.find_one({"_id": ObjectId(id)})
            
            return converterUtil.post_converter(updated_post)
        

    async def list_posts(self):
        found_posts = post_collection.aggregate([{
            "$lookup": {
                "from": "user", 
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }
        }])
        
        posts = []
        
        async for post in found_posts:
            posts.append(converterUtil.post_converter(post))
            
        return posts
        
        
    async def find_post(self, id: str):
        post = await post_collection.find_one({"_id": ObjectId(id)})
        
        if post:
            return converterUtil.post_converter(post)
        
        
    async def delete_post(self, id: str):
        post = await post_collection.find_one({"_id": ObjectId(id)})
        
        if post:
            await post_collection.delete_one({"_id": ObjectId(id)})