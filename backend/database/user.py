import bcrypt

from flask_login import UserMixin
from backend.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=True)
    profile_picture_url = db.Column(db.String, unique=False, nullable=True)
    account_source = db.Column(db.String, unique=False, nullable=False)


    def __init__(self, name, email, profile_picture_url, account_source):
        self.name = name
        self.email = email
        self.profile_picture_url = profile_picture_url
        self.account_source = account_source

    def set_password(self, password):
        self.password = bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=self.password)

    @classmethod
    def find_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_by_id(cls, record_id):
        return cls.query.get(record_id=record_id)

    @classmethod
    def find_by_email(cls, email):
        return db.session.query(cls).filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
