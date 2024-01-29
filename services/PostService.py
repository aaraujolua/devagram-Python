from providers.AWSProvider import AWSProvider
from repositories.PostRepository import PostRepository
from models.PostModel import PostCreateModel
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
		        "msg": "Erro interno no servidor",
		        "data": str(error),
		        "status": 500
		    }