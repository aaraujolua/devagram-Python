from fastapi import APIRouter, Body, HTTPException
from models.UserModel import UserCreateModel
from services.UserService import register_user

router = APIRouter()

@router.post("/", response_description='Route to create a new user')
async def route_create_new_user(user: UserCreateModel = Body(...)):
    result = await register_user(user)
    
    if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['msg'])
    
    return result