from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

# from flask_login import UserMixin
# from flask_sqlalchemy import SQLAlchemy


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
