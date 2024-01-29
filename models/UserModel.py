from pydantic import BaseModel, Field, EmailStr
from fastapi import UploadFile
from utils.DecoratorUtil import DecoratorUtil


decoratorUtil = DecoratorUtil()


class UserModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)  
    password: str = Field (...)
    icon: str = Field(...)
    
    
    class Config:
        extra_schema = {
            "user": {
                    "name": "Luana",
                    "email": "f.araujoluana@gmail.com",
                    "password": "123lua",
                    "icon": "lua.jpg"
            }
        }


@decoratorUtil.form_body
class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)  
    password: str = Field (...)
    
    class Config:
        extra_schema = {
            "user": {
                    "name": "Luana",
                    "email": "f.araujoluana@gmail.com",
                    "password": "123lua",
                    "icon": "lua.jpg"
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