import jwt
import time
from decouple import config
from utils.AuthUtil import verify_password
from models.UserModel import UserLoginModel
from repositories.UserRepository import UserRepository

JWT_SECRET = config('JWT_SECRET')

userRepository = UserRepository()

def generate_token_jwt(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    return token


def decode_token_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms="HS256")
        
        if decoded_token["expires"] >= time.time():
            return decoded_token
        
        else:
            return None
    
    except Exception as error:
            return None


async def login_service(user: UserLoginModel):
    user_found = await userRepository.find_user_by_email(user.email)

    if not user_found:
        return {
            "msg": "Incorrect email or password",
            "status": 401
        }
        
    else:
        if verify_password(user.password, user_found['password']):
            return {
                "msg": "Login successful!",
                "data": user_found,
                "status": 200
            }
            
        else: 
            return {
                "msg": "Incorrect email or password",
                "status": 401
            }