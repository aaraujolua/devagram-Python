from fastapi import APIRouter, Body, HTTPException, Depends, Header
from models.UserModel import UserCreateModel
from services.UserService import register_user, find_current_user
from middlewares.JWTMiddleware import verify_token
from services.AuthService import decode_token_jwt

router = APIRouter()

@router.post("/", response_description='Route to create a new user')
async def route_create_new_user(user: UserCreateModel = Body(...)):
    try:
        result = await register_user(user)
    
        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['msg'])
        
        return result
    
    except Exception as error:
        raise HTTPException(status_code=500, detail='Internal server error')
        

@router.get("/me", response_description='Route to search info from the current user', dependencies=[Depends(verify_token)])
async def search_info_current_user(Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        
        payload = decode_token_jwt(token)
        
        result = await find_current_user(payload["user_id"])
        
        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['msg'])
        
        return result
        
    except Exception as error:
        raise HTTPException(status_code=500, detail='Internal server error')