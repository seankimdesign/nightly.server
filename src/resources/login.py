from flask import request
from flask_restful import Resource
from models.user import UserModel


class Login(Resource):

    def post(self, username):
        given_password = request.json.get('password')
        if given_password is None:
            return {"message": "Invalid request"}, 400
        user = UserModel.retrieve_by_username(username)
        if user:
            hashed, _ = UserModel.hash_password(given_password, user.salt)
            if hashed == user.password:
                return {
                    "message": "Login successful",
                    "auth_token": "token goes here"
                }
        return {"message": "Username and password combination did not match any records"}, 401
