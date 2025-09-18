from flask_login import UserMixin
from sqlalchemy.sql import func

from .db import get_db


class User(UserMixin):
    def __init__(self, id_, username, email, password, profile_pic) -> None:
        self.id = id_
        self.username = username
        self.email = email
        self.password = password
        self.profile_pic = profile_pic

        @staticmethod
        def get(user_email):
            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE email=?;", (user_email).fetchone()
            )
            if not user:
                return None

            user = User(
                id_=user[0],
                username=user[1],
                email=user[3],
                password=user[4],
                profile_pic=user[5],
            )
            return user

        @staticmethod
        def create(id_, username, email, password, profile_pic):
            db = get_db()
            db.execute(
                "INSERT INTO users(id,username,email,password,profile_pic) VALUES (?,?,?,?,?);"
            )
            db.commit()
