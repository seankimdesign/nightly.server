from hashlib import sha256
from secrets import token_hex
from datetime import datetime

from db import db

# TODO: Implement via configuration
from temp_pepper import pepper


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    salt = db.Column(db.String(32))
    is_validated = db.Column(db.Boolean())
    created = db.Column(db.String(50))
    refresh_jti = db.Column(db.String(36))
    journals = db.relationship("JournalModel", backref="users", lazy=True, order_by="JournalModel.date")

    def __init__(self, username, password, name, email, is_validated=False):
        self.username = username
        self.password, self.salt = UserModel.hash_password(password)
        self.name = name
        self.email = email
        self.is_validated = is_validated
        self.created = datetime.now()
        self.refresh_jti = ""

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "created": self.created,
        }

    @classmethod
    def retrieve_by_username(cls, username):
        if username:
            return cls.query.filter_by(username=username).first()

    @classmethod
    def retrieve_by_email(cls, email):
        if email:
            return cls.query.filter_by(email=email).first()

    @classmethod
    def retrieve_by_id(cls, _id):
        if _id:
            return cls.query.filter_by(id=_id).first()

    @classmethod
    def hash_password(cls, password, salt=None):
        if salt is None:
            salt = token_hex(16)
        hash_fn = sha256()
        hash_fn.update((str(password)+salt+pepper).encode())
        return hash_fn.hexdigest(), salt
