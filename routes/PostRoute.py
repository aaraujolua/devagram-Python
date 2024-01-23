from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from models.PostModel import PostCreateModel
from datetime import datetime
import os
from middlewares.JWTMiddleware import verify_token


router = APIRouter()

@router.post("/", response_description='Route to create a new post')
async def route_create_post(file: UploadFile, user: PostCreateModel = Depends(PostCreateModel)):
    try:
        file_location = f'files/photo-{datetime.now().strftime("%H%M%S")}.jpg'
        
        with open(file_location,'wb+') as files:
            files.write(file.file.read())
        
        #result = await register_user(user, file_location)
    
        os.remove(file_location)
    
    except Exception as error:
        raise error
        
@router.get("/", response_description="Route to list the posts.", dependencies=[Depends(verify_token)])
async def list_posts(Authorization: str = Header(default='')):
    try:
        
        return {
            "test": "OK"
        }
        
    except Exception as error:
        raise error


@router.get("/me", response_description="Route to list the current user's posts.", dependencies=[Depends(verify_token)])
async def search_current_user_posts(Authorization: str = Header(default='')):
    try:
        
        return {
            "test": "OK"
        }
        
    except Exception as error:
        raise error