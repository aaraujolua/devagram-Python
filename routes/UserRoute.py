import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile

from services.UserService import UserService
from services.AuthService import AuthService
from middlewares.JWTMiddleware import verify_token
from models.UserModel import UserCreateModel, UserUpdateModel


router = APIRouter()
userService = UserService()
authService = AuthService()


@router.post("/", response_description='Route to create a new user.')
async def route_create_new_user(file: UploadFile, user: UserCreateModel = Depends(UserCreateModel)):
    try:
        file_location = f'files/photo-{datetime.now().strftime("%H%M%S")}.jpg'
        
        with open(file_location,'wb+') as files:
            files.write(file.file.read())
        
        result = await userService.register_user(user, file_location)
    
        os.remove(file_location)
        
        if not result.status == 201:
            raise HTTPException(status_code=result.status, detail=result.msg)
        
        return result
    
    except Exception as error:
        raise error
        

@router.get("/", response_description='Route to list all users.', dependencies=[Depends(verify_token)])
async def list_users(name: str):
    try:
        result = await userService.list_users(name) 
        
        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.msg)
        
        return result
        
    except Exception as error:
        raise error
    

@router.get("/me", response_description='Route to search info from the current user.', dependencies=[Depends(verify_token)])
async def search_current_user_info(Authorization: str = Header(default='')):
    try:
        current_user = await authService.find_current_user(Authorization)
        
        result = await userService.find_user(current_user.id)
        
        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.msg)
        
        return result
        
    except Exception as error:
        raise error
    
    
@router.get("/{user_id}", response_description="Route to search a user's info.", dependencies=[Depends(verify_token)])
async def search_user_info(user_id: str):
    try:
        result = await userService.find_user(user_id)
        
        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.msg)
        
        return result
        
    except Exception as error:
        raise error


@router.put("/me", response_description='Route to update info from the current user.', dependencies=[Depends(verify_token)])
async def update_current_user_info(Authorization: str = Header(default=''), user_update: UserUpdateModel = Depends(UserUpdateModel)):
    try:
        current_user = await authService.find_current_user(Authorization)

        result = await userService.update_current_user(current_user.id, user_update)
        
        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.msg)
        
        return result
        
    except Exception as error:
        raise error
    
    
@router.put('/follow/{user_id}', response_description="Route to follow/unfollow a user.", dependencies=[Depends(verify_token)])
async def follow_unfollow_userr(user_id: str, Authorization: str = Header(default="")):        
    current_user = await authService.find_current_user(Authorization)
        
    result = await userService.follow_unfollow(current_user.id, user_id)
    
    if not result.status == 200:
        raise HTTPException(status_code=result.status, detail=result.msg)

    return result