from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti

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
                refresh_token = create_refresh_token(user)
                refresh_jti = get_jti(refresh_token)
                user.refresh_jti = refresh_jti
                user.save_to_db()
                return {
                    "message": "Login successful",
                    "access_token": create_access_token(user),
                    # TODO: Use Set-Cookie for improved security
                    "refresh_token": refresh_token
                }
        return {"message": "Username and password combination did not match any records"}, 401
