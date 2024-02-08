from pydantic import BaseModel, Field
from typing import List
from models.UserModel import UserModel
from fastapi import UploadFile
from utils.DecoratorUtil import DecoratorUtil


decoratorUtil = DecoratorUtil()


class PostModel(BaseModel):
    id: str = Field(...)
    user: UserModel = Field(...)
    photo: str = Field(...)
    legend: str = Field(...)
    date: str = Field(...)
    likes: List = Field(...)
    comments: List = Field(...)

    class Config:
            extra_schema = {
                "post": {
                        "id": "string",
                        "user": "UserModel",    
                        "photo": "string",
                        "legend": "string",
                        "date": "date",
                        "likes": "List[likes]",
                        "comments": "List[comments]"
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
        