from pydantic import BaseModel, Field, EmailStr
from fastapi import Form, UploadFile

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


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters = [
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )

    return cls

@form_body
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
        
@form_body
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