from typing import List
from fastapi import UploadFile
from pydantic import BaseModel, Field, EmailStr

from utils.DecoratorUtil import DecoratorUtil


decoratorUtil = DecoratorUtil()


class UserModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)  
    password: str = Field(...)
    icon: str = Field(...)
    followers: List
    following: List
    total_followers: int
    total_following: int
    posts: List
    total_posts: int
    token: str
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    class Config:
        extra_schema = {
            "user": {
                "id": "string",
                "name": "string",
                "email": "string",
                "password": "string",
                "icon": "string",
                "followers": "List",
                "following": "List",
                "total_followers": "int",
                "total_following": "int",
                "posts": "List",
                "total_posts": "int",
                "token": "string"
            }
        }
        

class UserExportModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...) 
    icon: str = Field(...)
    followers: List
    following: List
    total_followers: int
    total_following: int
    posts: List
    total_posts: int
    
    
    class Config:
        extra_schema = {
            "user": {
                "name": "string",
                "email": "string",
                "icon": "string",
                "followers": "List",
                "following": "List",
                "total_followers": "int",
                "total_following": "int",
                "posts": "List",
                "total_posts": "int",
            }
        }


@decoratorUtil.form_body
class UserCreateModel(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr = Field(...)  
    password: str = Field (...)
    
    class Config:
        extra_schema = {
            "user": {
                "name": "Luana",
                "email": "f.araujoluana@gmail.com",
                "password": "123lua",
            }
        }
        

class UserLoginModel(BaseModel):
    email: EmailStr = Field(...)  
    password: str = Field (...)
    
    class Config:
        extra_schema = {
            "user": {
                "email": "f.araujoluana@gmail.com",
                "password": "123lua",
            }
        }
        
@decoratorUtil.form_body
class UserUpdateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)  
    password: str = Field(...)
    icon: UploadFile = Field(...)
    
    class Config:
        extra_schema = {
            "user": {
                "name": "Luana",
                "email": "f.araujoluana@gmail.com",
                "password": "123lua",
                "icon": "lua.jpg"
            }
        }