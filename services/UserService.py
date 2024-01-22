from models.UserModel import UserCreateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import create_user, find_user_by_email, list_users, find_user, update_user, delete_user

awsProvider = AWSProvider()

async def register_user(user: UserCreateModel, file_location):
    try:
        user_found = await find_user_by_email(user.email)
        
        if user_found:
            return {
                "msg": f"E-mail '{user.email}' alredy has been registered.",
                "status": 400
            }
            
        else:
            new_user = await create_user(user)
            
            try:
                icon_url = awsProvider.upload_file_s3(f'photos-profile/{new_user["id"]}.jpg', file_location)
                
                new_user = await update_user(new_user["id"], {"icon": icon_url})
                
                print(new_user)
                
            except Exception as error:
                print(error)
            
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
        
async def find_current_user(id: str):
    try:
        user_found = await find_user(id)
        
        if user_found:
            return {
                "msg": f"User '{id}' found successfully!",
                "data": user_found,
                "status": 200
            }
            
        else:
            return {
                "msg": f"User '{id}' not found",
                "status": 404
            }
        
    except Exception as error:
        return {
            "msg": "Internal server error",
            "status": 500
        }