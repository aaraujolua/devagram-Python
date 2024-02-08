from pydantic import BaseModel, Field


class CommentModel(BaseModel):
    user_id: str = Field(...)
    comment: str = Field(...)
    

class CommentCreateModel(BaseModel):
    comment: str = Field(...)