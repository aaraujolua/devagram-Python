class ConverterUtil:
    def user_converter(self, user):
        return {
            "id": str(user["_id"]),
            "name": user['name'],
            "email": user['email'] ,
            "password": user['password'],
            "icon": user['icon'] if "icon" in user else ""
        }


    def post_converter(self, post):
        return {
            "id": str(post["_id"]) if "id" in post else "",
            "user": post['user'] if "user" in post else "",
            "photo": post['icon'] if "photo" in post else "",
            "legend": post['legend'] if "legend" in post else "",
            "date": post['date'] if "date" in post else "",
            "likes": post['likes'] if "likes" in post else "",
            "comments": post['comments'] if "comments" in post else "",
        }