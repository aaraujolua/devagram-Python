from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, Body
from models.PostModel import PostCreateModel
from datetime import datetime
import os
from middlewares.JWTMiddleware import verify_token
from services.AuthService import decode_token_jwt
from services.UserService import UserService
from services.PostService import PostService
from models.CommentModel import CommentCreateModel, CommentUpdateModel


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
    
        if not result.status == 201:
            raise HTTPException(status_code=result.status, detail=result.msg)
        
        return result
        
    except Exception as error:
        raise error


@router.get("/", response_description="Route to list the posts.", dependencies=[Depends(verify_token)])
async def list_posts():
    try:
        result = await postService.list_posts()
        
        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.msg) 
        
        return result
        
    except Exception as error:
        raise error
    
    
@router.get("/{user_id}", response_description="Route to list a user's posts.", dependencies=[Depends(verify_token)])
async def list_user_posts(user_id: str):
    try:
        result = await postService.list_user_posts(user_id)
        
        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.msg) 
        
        return result
        
    except Exception as error:
        raise error


@router.put('/like/{post_id}', response_description="Route to like/unlike a post.", dependencies=[Depends(verify_token)])
async def like_unlike_post(post_id: str, Authorization: str = Header(default="")):
    token = Authorization.split(' ')[1]
    
    payload = decode_token_jwt(token)
        
    user_result = await userService.find_current_user(payload["user_id"])
        
    current_user = user_result["data"]
        
    result = await postService.like_unlike(post_id, current_user["id"])
    
    if not result.status == 200:
        raise HTTPException(status_code=result.status, detail=result.msg)

    return result


@router.put('/comment/{post_id}', response_description="Route to create a comment on a post.", dependencies=[Depends(verify_token)])
async def comment_post(post_id: str, Authorization: str = Header(default=""), comment_model: CommentCreateModel = Body(...)):
    token = Authorization.split(' ')[1]

    payload = decode_token_jwt(token)
        
    user_result = await userService.find_current_user(payload["user_id"])
        
    current_user = user_result["data"]
        
    result = await postService.create_comment(post_id, current_user["id"], comment_model.comment)
    
    if not result.status == 200:
        raise HTTPException(status_code=result.status, detail=result.msg)

    return result


@router.delete('/{post_id}/comment/{comment_id}', response_description="Route to delete a comment on a post.", dependencies=[Depends(verify_token)])
async def delete_comment(post_id: str, comment_id: str, Authorization: str = Header(default="")):
    token = Authorization.split(' ')[1]

    payload = decode_token_jwt(token)   
        
    user_result = await userService.find_current_user(payload["user_id"])
        
    current_user = user_result["data"]
        
    result = await postService.delete_comment(post_id, current_user["id"], comment_id)
    
    if not result.status == 200:
        raise HTTPException(status_code=result.status, detail=result.msg)

    return result


@router.put('/{post_id}/comment/{comment_id}', response_description="Route to update a comment on a post.", dependencies=[Depends(verify_token)])
async def update_comment(post_id: str, comment_id: str, Authorization: str = Header(default=""), comment_model: CommentUpdateModel = Body(...)):
    token = Authorization.split(' ')[1]

    payload = decode_token_jwt(token)   
        
    user_result = await userService.find_current_user(payload["user_id"])
        
    current_user = user_result["data"]
        
    result = await postService.update_comment(post_id, current_user["id"], comment_id, comment_model.comment)
    
    if not result.status == 200:
        raise HTTPException(status_code=result.status, detail=result.msg)

    return result


@router.delete('/{post_id}', response_description="Route to delete a post.", dependencies=[Depends(verify_token)])
async def delete_post(post_id: str, Authorization: str = Header(default="")):
    token = Authorization.split(' ')[1]

    payload = decode_token_jwt(token)
        
    user_result = await userService.find_current_user(payload["user_id"])
        
    current_user = user_result["data"]
        
    result = await postService.delete_post(post_id, current_user["id"])
    
    if not result.status == 200:
        raise HTTPException(status_code=result.status, detail=result.msg)

    return result
        