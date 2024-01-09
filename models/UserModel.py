from pydantic import BaseModel, Field, EmailStr

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


class UserCreateModel(BaseModel):
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