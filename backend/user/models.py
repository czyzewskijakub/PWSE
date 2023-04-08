import bcrypt
from flask_login import UserMixin
from typing import Type, Optional, TypeVar

from backend.extensions import db

T = TypeVar("T", bound="UserModel")


class UserModel(db.Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        return cls.query.get(record_id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_all(cls):
        """Returns all the record from given table."""
        return db.session.query(cls).all()


class User(UserMixin, UserModel):
    __tablename__ = "users"
    email = db.Column(db.String(80))
    password = db.Column("password", db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def check_password(self, password):
        encoded_password = password.encode("utf-8")
        encoded_hashed_password = self.password.encode("utf-8")
        return bcrypt.checkpw(encoded_password, encoded_hashed_password)

    def __repr__(self):
        return f"<User({self.email!r})"

