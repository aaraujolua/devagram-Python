from fastapi import APIRouter, Body
from models.UserModel import UserModel
from repositories.UserRepository import create_user

router = APIRouter()

@router.post("/", response_description='Route to create a new user')
async def route_create_new_user(user: UserModel = Body(...)):
    result = await create_user(user)
    
    return {"msg": "User sucessfully registered!"}, result