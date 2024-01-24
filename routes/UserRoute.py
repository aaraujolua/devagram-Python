from fastapi import APIRouter, Body, HTTPException, Depends, Header, UploadFile
from datetime import datetime
import os
from models.UserModel import UserCreateModel, UserUpdateModel
from services.UserService import UserService
from middlewares.JWTMiddleware import verify_token
from services.AuthService import decode_token_jwt



router = APIRouter()

userService = UserService()

@router.post("/", response_description='Route to create a new user')
async def route_create_new_user(file: UploadFile, user: UserCreateModel = Depends(UserCreateModel)):
    try:
        file_location = f'files/photo-{datetime.now().strftime("%H%M%S")}.jpg'
        
        with open(file_location,'wb+') as files:
            files.write(file.file.read())
        
        result = await userService.register_user(user, file_location)
    
        os.remove(file_location)
        
        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['msg'])
        
        return result
    
    except Exception as error:
        raise error
        

@router.get("/me", response_description='Route to search info from the current user', dependencies=[Depends(verify_token)])
async def search_current_user_info(Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        
        payload = decode_token_jwt(token)
        
        result = await userService.find_current_user(payload["user_id"])
        
        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['msg'])
        
        return result
        
    except Exception as error:
        raise error
    

@router.put("/me", response_description='Route to update info from the current user', dependencies=[Depends(verify_token)])
async def update_current_user_info(Authorization: str = Header(default=''), user_update: UserUpdateModel = Depends(UserUpdateModel)):
    try:
        token = Authorization.split(' ')[1]
        
        payload = decode_token_jwt(token)
        
        result = await userService.update_current_user(payload["user_id"], user_update)
        
        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['msg'])
        
        return result
        
    except Exception as error:
        raise error