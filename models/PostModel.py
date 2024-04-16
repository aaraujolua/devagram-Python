from fastapi import UploadFile
from typing import List, Optional
from pydantic import BaseModel, Field

from models.UserModel import UserModel
from utils.DecoratorUtil import DecoratorUtil


decoratorUtil = DecoratorUtil()


class PostModel(BaseModel):
    id: str = Field(...)
    user_id: str = Field(...)
    photo: str = Field(...)
    legend: str = Field(...)
    date: str = Field(...)
    likes: List
    comments: List
    user: Optional[UserModel]
    total_likes: int
    total_comments: int
    
    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        extra_schema = {
            "post": {
                "id": "string",
                "user_id": "string",    
                "photo": "string",
                "legend": "string",
                "date": "date",
                "likes": "List[likes]",
                "comments": "List[comments]",
                "user": "Optional[UserModel]",
                "total_likes": "int",
                "total_comments": "int"
            }
        }
        
@decoratorUtil.form_body
class PostCreateModel(BaseModel):
    photo: UploadFile = Field(...)
    legend: str = Field(...)
    
    class Config:
            extra_schema = {
                "post": {
                    "photo": "string",
                    "legend": "string",
                }
            }
        