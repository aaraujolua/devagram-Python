from models.PostModel import PostModel
from models.UserModel import UserModel, UserExportModel


class ConverterUtil:
    def user_converter(self, user):
        return UserModel(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"] ,
            password=user["password"],
            icon=user["icon"] if "icon" in user else "",
            followers=[str(l) for l in user["followers"]] if "followers" in user else [],
            following=[str(l) for l in user["following"]] if "following" in user else [],
            total_followers=user["total_followers"] if "total_followers" in user else 0,
            total_following=user["total_following"]if "total_following" in user else 0,
            posts=user["posts"] if "posts" in user else [],
            total_posts=user["total_posts"] if "total_posts" in user else 0,
            token=user["token"] if "token" in user else ""    
        )
        
        
    def user_export_converter(self, user):
        return UserExportModel(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"] ,
            icon=user["icon"] if "icon" in user else "",
            followers=[str(l) for l in user["followers"]] if "followers" in user else [],
            following=[str(l) for l in user["following"]] if "following" in user else [],
            total_followers=user["total_followers"] if "total_followers" in user else 0,
            total_following=user["total_following"]if "total_following" in user else 0,
            posts=user["posts"] if "posts" in user else [],
            total_posts=user["total_posts"] if "total_posts" in user else 0, 
        )


    def post_converter(self, post):
        return PostModel(
            id=str(post["_id"]) if "_id" in post else "",
            user_id=str(post["user_id"]) if "user_id" in post else "",
            photo=post["photo"] if "photo" in post else "",
            legend=post["legend"] if "legend" in post else "",
            date=post["date"] if "date" in post else "",
            likes=[str(l) for l in post["likes"]] if "likes" in post else [],
            comments= [
                {
                    "comment": c["comment"],
                    "comment_id": str(c["comment_id"]),
                    "user_id": str(c["user_id"])
                } for c in post["comments"]
            ] if "comments" in post else "",
            usuer=self.user_converter(post["user"][0]) if "user" in post and len(post["user"]) > 0 else None,
            total_likes=post["total_likes"] if "total_likes" in post else 0,
            total_comments=post["total_comments"] if "total_comments" in post else 0,
        )