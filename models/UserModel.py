from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)  
    password: str = Field (...)
    icon: str = Field(...)
    
    
class Sett:
    extra_schema = {
        "user": {
                "name": "Luana",
                "email": "f.araujoluana@gmail.com",
                "password": "123lua",
                "icon": "lua.jpg"
        }
    }
    
    #oq ssignifica fieles no codigo?