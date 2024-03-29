class ConverterUtil:
    def user_converter(self, user):
        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"] ,
            "password": user["password"],
            "icon": user["icon"] if "icon" in user else "",
            "followers": [str(l) for l in user["followers"]] if "followers" in user else "",
            "following": [str(l) for l in user["following"]] if "following" in user else ""   
        }


    def post_converter(self, post):
        return {
            "id": str(post["_id"]) if "_id" in post else "",
            "user_id": str(post["user_id"]) if "user_id" in post else "",
            "photo": post["photo"] if "photo" in post else "",
            "legend": post["legend"] if "legend" in post else "",
            "date": post["date"] if "date" in post else "",
            "likes": [str(l) for l in post["likes"]] if "likes" in post else "",
            "comments": [
                {
                    "comment": c["comment"],
                    "comment_id": str(c["comment_id"]),
                    "user_id": str(c["user_id"])
                }
                for c in post["comments"]] if "comments" in post else "",
                "user": self.user_converter(post["user"][0]) if "user" in post and len(post["user"]) > 0 else ""
        }