import jwt
import time
from decouple import config
from utils.AuthUtil import AuthUtil
from models.UserModel import UserLoginModel, UserModel
from repositories.UserRepository import UserRepository
from dtos.ResponseDTO import ResponseDTO
from services.UserService import UserService


JWT_SECRET = config('JWT_SECRET')

userRepository = UserRepository()

authUtil = AuthUtil()

userService = UserService()

class AuthService():

    def generate_token_jwt(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 6000
        }
        
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        
        return token


    def decode_token_jwt(self, token: str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms="HS256")
            
            if decoded_token["expires"] >= time.time():
                return decoded_token
            
            else:
                return None
        
        except Exception as error:
                return None


    async def login_service(self, user: UserLoginModel):
        user_found = await userRepository.find_user_by_email(user.email)

        if not user_found:
            return ResponseDTO("Incorrect email or password", "", 401)
            
        else:
            if authUtil.verify_password(user.password, user_found.password):
                return ResponseDTO("Login successful!", user_found, 200)
                
            else: 
                return ResponseDTO("Incorrect email or password", "", 401)
        
        
    async def find_current_user(self, Authorization: str) -> UserModel:
        token = Authorization.split(' ')[1]
    
        payload = self.decode_token_jwt(token)

        user_result = await userService.find_user(payload["user_id"])
        
        current_user = user_result.data
        
        return current_user