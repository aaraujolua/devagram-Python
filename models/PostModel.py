from pydantic import BaseModel, Field
from typing import List
from models.CommentModel import CommentModel
from models.UserModel import UserModel


class PostModel(BaseModel):
    id: str = Field(...)
    user: UserModel = Field(...)
    photo: str = Field(...)
    legend: str = Field(...)
    date: str = Field(...)
    likes: int = Field(...)
    comments: List[CommentModel] = Field(...)

    class Config:
            extra_schema = {
                "post": {
                        "id": "string",
                        "user": "UserModel",    
                        "photo": "string",
                        "legend": "string",
                        "date": "date",
                        "likes": "int",
                        "comments": "List[comments]"
                }
            }
        

class PostCreateModel(BaseModel):
    user: UserModel = Field(...)
    photo: str = Field(...)
    legend: str = Field(...)
    
    class Config:
            extra_schema = {
                "post": {
                        "user": "UserModel",
                        "photo": "string",
                        "legend": "string",
                }
            }
        