from models.UserModel import UserCreateModel
from decouple import config
import motor.motor_asyncio
from bson import ObjectId
from utils.AuthUtil import encrypt_password

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

user_collection = database.get_collection("user")

def show_user_data(user):
     return {
        "id": str(user["_id"]),
        "name": user['name'],
        "email": user['email'] ,
        "password": user['password'],
        "icon": user['icon'] if "icon" in user else ""
    }


async def create_user(user: UserCreateModel) -> dict:
    user.password = encrypt_password(user.password)
     
    created_user = await user_collection.insert_one(user.__dict__)
    
    new_user = await user_collection.find_one({"_id": created_user.inserted_id})
    
    return show_user_data(new_user)
    
    
async def list_users():
    return user_collection.find()
    
    
async def find_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    
    if user:
        return show_user_data(user)

    
async def find_user_by_email(email: str) -> dict:
    user = await user_collection.find_one({"email": email})
    
    if user:
        return show_user_data(user)
    

async def update_user(id: str, user_data: dict):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    
    if user:
        updated_user = await user_collection.update_one({"_id": ObjectId(id)}, {"$set"})
        
        found_user = await user_collection.find_one({
            {"_id": ObjectId(id)}
        })

        return {"msg": "User sucessfully updated!"}, show_user_data(found_user)
    
    
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
    