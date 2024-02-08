from models.UserModel import UserCreateModel, UserUpdateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import UserRepository
from bson import ObjectId
from datetime import datetime
import os


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
                    
                    os.remove(file_location)
                    
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
            
            
    async def follow_unfollow(self, current_user_id, user_id):
        try:
            found_user = await userRepository.find_user(user_id)
            current_user = await userRepository.find_user(current_user_id)

            if not found_user:
                return {
                    "msg": "User not found",
                    "status": 404
                }

            if current_user_id in found_user["followers"] and user_id in current_user["following"]:
                found_user["followers"].remove(current_user_id)
                current_user["following"].remove(user_id)

                action_msg = "You unfollowed this user."
            else:
                found_user["followers"].append(ObjectId(current_user_id))
                current_user["following"].append(ObjectId(user_id))
                
                action_msg = "Now you are following this user!"


            await userRepository.update_user(found_user["id"], {"followers": found_user["followers"]})
            await userRepository.update_user(current_user["id"], {"following": current_user["following"]})

            return {
                "msg": action_msg,
                "status": 200
            }

        except Exception as error:
            print(error)
            return {
                "msg": "Internal server error",
                "data": str(error),
                "status": 500
            }
