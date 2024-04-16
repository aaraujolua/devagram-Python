import os
from bson import ObjectId
from datetime import datetime

from dtos.ResponseDTO import ResponseDTO
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import UserRepository
from repositories.PostRepository import PostRepository
from models.UserModel import UserCreateModel, UserUpdateModel, UserExportModel


awsProvider = AWSProvider()
userRepository = UserRepository()
postRepository = PostRepository()


class UserService:

    async def register_user(self, user: UserCreateModel, file_location):
        try:
            found_user = await userRepository.find_user_by_email(user.email)
            
            if found_user:
                return ResponseDTO(f"'{user.email}' alredy has been registered.", "", 400)
             
            else:
                new_user = await userRepository.create_user(user)
                
                try:
                    icon_url = awsProvider.upload_file_s3(f'profile-photos/{new_user.id}.jpg', file_location)
                    
                except Exception as error:
                    print(error)
                
                new_user = await userRepository.update_user(new_user.id, {"icon": icon_url}) 
                
                return ResponseDTO("User sucessfully registered!", new_user, 201)
                    
        except Exception as error:
            return ResponseDTO("Internal server error", "", 500)
            
            
    async def list_users(self, name):
        try:
            found_users = await userRepository.list_users(name)
            
            for user in found_users:
                user.total_followers = len(user.followers)
                user.total_following = len(user.following)
            
            return ResponseDTO("Listed users:", found_users, 200)
                
        except Exception as error:
            return ResponseDTO("Internal server error", str(error), 500)
    
    
    async def find_user(self, id: str):
        try:
            found_user = await userRepository.find_user(id)
            
            if found_user:
                found_posts = await postRepository.list_user_posts(id)
                
                found_user.total_followers = len(found_user.followers)
                found_user.total_following = len(found_user.following)
                found_user.posts = found_posts
                found_user.total_posts = len(found_posts)
                
                return ResponseDTO("User found successfully!", found_user, 200)
                
            else:
                return ResponseDTO(f"User not found", "", 404)
            
        except Exception as error:
            return ResponseDTO("Internal server error", str(error), 500)
        
    
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
                    return ResponseDTO("Internal server error", str(error), 500)
                    
                user_dict['icon'] = icon_url if icon_url is not None else user_dict['icon']
                
                user_updated = await userRepository.update_user(id, user_dict)
                
                return ResponseDTO("User successfully updated!", user_updated, 200)
                
            else:
                return ResponseDTO("User not found", "", 404)
        
        except Exception as error:
            return ResponseDTO("Internal server error", str(error), 500)
            
            
    async def follow_unfollow(self, current_user_id, user_id):
        try:
            found_user = await userRepository.find_user(user_id)
            current_user = await userRepository.find_user(current_user_id)

            if not found_user:
                return ResponseDTO("User not found", "", 404)

            if current_user_id in found_user.followers and user_id in current_user.following:
                found_user.followers.remove(current_user_id)
                current_user.following.remove(user_id)

                action_msg = "You unfollowed this user."
            else:
                found_user.followers.append(ObjectId(current_user_id))
                current_user.following.append(ObjectId(user_id))
                
                action_msg = "Now you are following this user!"


            await userRepository.update_user(found_user.id, {"followers": found_user["followers"]})
            await userRepository.update_user(current_user.id, {"following": current_user["following"]})

            return ResponseDTO(action_msg, "", 200)

        except Exception as error:
            return ResponseDTO("Internal server error", str(error), 500)

