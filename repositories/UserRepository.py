from models.UserModel import UserCreateModel
from decouple import config
import motor.motor_asyncio
from bson import ObjectId
from utils.AuthUtil import encrypt_password
from utils.ConverterUtil import ConverterUtil

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

user_collection = database.get_collection("user")

converterUtil = ConverterUtil()

class UserRepository:

    async def create_user(self, user: UserCreateModel) -> dict:
        user.password = encrypt_password(user.password)
        
        user_dict = {
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "followers": [],
            "following": []
        }
        
        created_user = await user_collection.insert_one(user_dict)
        
        new_user = await user_collection.find_one({"_id": created_user.inserted_id})
        
        return converterUtil.user_converter(new_user)
        
        
    async def list_users(self):
        found_users = user_collection.find()
        
        users = []
        
        async for user in found_users:
            users.append(converterUtil.user_converter(user))
            
        return users
        
        
    async def find_user(self, id: str):
        user = await user_collection.find_one({"_id": ObjectId(id)})
        
        if user:
            return converterUtil.user_converter(user)

        
    async def find_user_by_email(self, email: str) -> dict:
        user = await user_collection.find_one({"email": email})
        
        if user:
            return converterUtil.user_converter(user)
        

    async def update_user(self, id: str, user_data: dict):
        if "password" in user_data:
            user_data["password"] = encrypt_password(user_data['password'])
        
        user = await user_collection.find_one({"_id": ObjectId(id)})
        
        if user:
            await user_collection.update_one({"_id": ObjectId(id)}, {"$set": user_data})
            
            found_user = await user_collection.find_one({"_id": ObjectId(id)})

            return converterUtil.user_converter(found_user)

        
    async def delete_user(self, id: str):
        user = await user_collection.find_one({"_id": ObjectId(id)})
        
        if user:
            await user_collection.delete_one({"_id": ObjectId(id)})
    