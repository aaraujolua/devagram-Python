from pydantic import BaseModel, Field
from models.UserModel import UserModel


class CommentModel(BaseModel):
    user: UserModel = Field(...)
    comment: str = Field(...)