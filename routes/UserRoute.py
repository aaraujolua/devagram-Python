from fastapi import APIRouter, Body
from models.UserModel import UserModel

router = APIRouter()

@router.post("/", response_description='Route to create a new user')
async def route_create_new_user(user: UserModel = Body(...)):
    return {
        "Msg": "User successfully registered!"
    }