from models.UserModel import UserCreateModel, UserUpdateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import UserRepository
from datetime import datetime


awsProvider = AWSProvider()

userRepository = UserRepository()


class UserService:

    async def register_user(self, user: UserCreateModel, file_location):
        try:
            user_found = await userRepository.find_user_by_email(user.email)
            
            if user_found:
                return {
                    "msg": f"E-mail '{user.email}' alredy has been registered.",
                    "status": 400
                }
                
            else:
                new_user = await userRepository.create_user(user)
                
                try:
                    icon_url = awsProvider.upload_file_s3(f'profile-photos/{new_user["id"]}.jpg', file_location)
                    
                except Exception as error:
                    print(error)
                
                new_user = await userRepository.update_user(new_user["id"], {"icon": icon_url}) 
                
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
            
    async def find_current_user(self, id: str):
        try:
            user_found = await userRepository.find_user(id)
            
            if user_found:
                return {
                    "msg": f"User found successfully!",
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
    
    
    async def update_current_user(self, id, user_update: UserUpdateModel):
        try: 
            user_found = await userRepository.find_user(id)
            
            if user_found:
                user_dict = user_update.__dict__
                
                try:
                    file_location = f'files/photo-{datetime.now().strftime("%H%M%S")}.jpg'
        
                    with open(file_location,'wb+') as files:
                        files.write(user_update.icon.file.read())
                    
                    icon_url = awsProvider.upload_file_s3(f'profile-photos/{id}.jpg', file_location)
                    
                except Exception as error:
                    print(error)
                    
                user_dict['icon'] = icon_url if icon_url is not None else user_dict['icon']
                
                user_updated = await userRepository.update_user(id, user_dict)
                
                return {
                    "msg": f"User successfully updated!",
                    "data": user_updated,
                    "status": 200
                }
                
            else:
                return {
                    "msg": f"User '{id}' not found",
                    "status": 404
                }
        
        except Exception as error:
            print(error)