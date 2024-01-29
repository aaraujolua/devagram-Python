from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from models.PostModel import PostCreateModel
from datetime import datetime
import os
from middlewares.JWTMiddleware import verify_token
from services.AuthService import decode_token_jwt
from services.UserService import UserService
from services.PostService import PostService


router = APIRouter()

userService = UserService()

postService = PostService()

@router.post("/", response_description='Route to create a new post',  dependencies=[Depends(verify_token)])
async def route_create_post(Authorization: str = Header(default=''), post: PostCreateModel = Depends(PostCreateModel)):
    try:
        
        token = Authorization.split(' ')[1]
        
        payload = decode_token_jwt(token)
        
        user_result = await userService.find_current_user(payload["user_id"])
        
        current_user = user_result["data"]
        
        result = await postService.make_post(post, current_user["id"])
    
        if not result["status"] == 201:
            raise HTTPException(status_code=result["status"], detail=result["msg"])
        
        return result 
        
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
