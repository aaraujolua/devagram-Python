from providers.AWSProvider import AWSProvider
from repositories.PostRepository import PostRepository
from models.PostModel import PostCreateModel
from bson import ObjectId
from datetime import datetime
import os


awsProvider = AWSProvider()

postRepository = PostRepository()


class PostService:

    async def make_post(self, post: PostCreateModel, user_id):
        try:
            created_post = await postRepository.create_post(post, user_id)
           
            try:
                file_location = f'files/photo-{datetime.now().strftime("%H%M%S")}.jpg'

                with open(file_location,'wb+') as filess:
                    filess.write(post.photo.file.read())
                    
                photo_url = awsProvider.upload_file_s3(f'post-photos/{created_post["id"]}.jpg', file_location)
                
                new_post = await postRepository.update_post(created_post["id"], {"photo": photo_url})
                
                os.remove(file_location)
                    
            except Exception as error:
                print(error)

            return {
                "msg": "Post created successfully!",
                "data": new_post,
                "status": 201
            }


        except Exception as error:
            print(error),
            return {
		        "msg": "Internal server error",
		        "data": str(error),
		        "status": 500
		    }
    
    
    async def list_posts(self):
        try:
            posts = await postRepository.list_posts()
            
            for p in posts:
                p["total_likes"] = len(p["likes"])
                p["total_comments"] = len(p["comments"])
            
            return {
                "msg": "Listed posts:",
                "data": posts,
                "status": 200
            }
            
            
        except Exception as error:
            print(error),
            return {
		        "msg": "Internal server error",
		        "data": str(error),
		        "status": 500
		    }
            
            
    async def list_user_posts(self, user_id):
        try:
            posts = await postRepository.list_user_posts(user_id)
            
            for p in posts:
                p["total_likes"] = len(p["likes"])
                p["total_comments"] = len(p["comments"])
            
            return {
                "msg": "Listed posts:",
                "data": posts,
                "status": 200
            }
            
            
        except Exception as error:
            print(error),
            return {
		        "msg": "Internal server error",
		        "data": str(error),
		        "status": 500
		    }
            
            
    async def like_unlike(self, post_id, user_id):
        try:
            found_post = await postRepository.find_post(post_id)
            
            if not found_post:
                return {
                    "msg": "Post not found",
                    "status": 404
                }
        
            if found_post["likes"].count(user_id) > 0:
                found_post["likes"].remove(user_id)
                action_msg = "Post unliked successfully!"
            else:
                found_post["likes"].append(ObjectId(user_id))
                action_msg = "Post liked successfully!"
            
            updated_post = await postRepository.update_post(found_post["id"], {"likes": found_post["likes"]})
            
            return {
                "msg": action_msg,
                "data": updated_post,
                "status": 200
            }
                

        except Exception as error:
            print(error),
            return {
		        "msg": "Internal server error",
		        "data": str(error),
		        "status": 500
		    }
    
    
    async def create_comment(self, post_id, user_id, comment):   
        try:
            found_post = await postRepository.find_post(post_id)
            
            if not found_post:
                return {
                    "msg": "Post not found",
                    "status": 404
                }
            
            found_post["comments"].append({
                "user_id": ObjectId(user_id),
                "comment": comment
            })
            
            updated_post = await postRepository.update_post(found_post["id"], {"comments": found_post["comments"]})

            return {
                "msg": "Post commented successfully!",
                "data": updated_post,
                "status": 200
            }


        except Exception as error:
            print(error),
            return {
		        "msg": "Internal server error",
		        "data": str(error),
		        "status": 500
		    }
            
            
    async def delete_post(self, post_id, user_id):   
        try:
            found_post = await postRepository.find_post(post_id)
            
            if not found_post:
                return {
                    "msg": "Post not found",
                    "status": 404
                }
            
            if not found_post["user_id"] == user_id:
            

                return {
                    "msg": "Unable action",
                    "status": 401
                }
                
            await postRepository.delete_post(post_id)
            
            return {
                "msg": "Post deleted successfully!",
                "status": 200
            }


        except Exception as error:
            print(error),
            return {
		        "msg": "Internal server error",
		        "data": str(error),
		        "status": 500
		    }
  
            