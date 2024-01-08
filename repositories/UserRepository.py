import motor.motor_asyncio
from models.UserModel import UserModel
from decouple import config

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

user_collection = database.get_collection("user")


async def create_user(user: UserModel) -> dict: 
    created_user = await user_collection.insert_one(user.__dict__)
    
    new_user = await user_collection.find_one({"_id": created_user.inserted_id})
    
    return {
        "name": new_user['name'],
        "email": new_user['email'],
        "password": new_user['password'],
        "icon": new_user['icon'],
    }
    
    