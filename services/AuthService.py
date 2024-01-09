from utils.AuthUtil import verify_password
from models.UserModel import UserLoginModel


async def login_service(user: UserLoginModel):
    from repositories.UserRepository import find_user_by_email
    user_found = await find_user_by_email(user.email)

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