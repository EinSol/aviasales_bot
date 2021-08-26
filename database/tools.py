from database.dbmodels import User, db
import json


def store_user(user_info):
    with db:
        User.create(uid=user_info['uid'],
                    username=user_info['username'],
                    name=user_info['name'],
                    phone=user_info['phone'],
                    application=json.dumps(user_info['wishlist']),
                    )
