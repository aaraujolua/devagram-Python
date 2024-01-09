from models.UserModel import UserCreateModel
from repositories.UserRepository import create_user, find_user_by_email, list_users, update_user, delete_user

async def register_user(user: UserCreateModel):
    try:
        user_found = await find_user_by_email(user.email)
        
        if user_found:
            return {
                "msg": f"E-mail '{user.email}' alredy has been registered.",
                "status": 400
            }
            
        else:
            new_user = await create_user(user)
            
            return {
                "msg": "User sucessfully registered!",
                "data": new_user,
                "status": 201
            }
                
    except Exception as error:
        return {
            "msg": "Internal server error",
            "status": 500
        }