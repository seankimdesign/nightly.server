from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jti,
    set_refresh_cookies, set_access_cookies
)

from models.user import UserModel


class Login(Resource):

    def post(self, username):
        print(request.cookies)
        print(request.json)
        given_password = request.json.get('password')
        if given_password is None:
            return {"message": "Invalid request"}, 400
        user = UserModel.retrieve_by_username(username)
        if user:
            hashed, _ = UserModel.hash_password(given_password, user.salt)
            if hashed == user.password:
                access_token = create_access_token(user, fresh=True)
                refresh_token = create_refresh_token(user)
                refresh_jti = get_jti(refresh_token)
                user.refresh_jti = refresh_jti
                user.save_to_db()
                resp = jsonify({
                    "message": "Login successful",
                    "access_token": access_token
                })
                set_access_cookies(resp, access_token)
                set_refresh_cookies(resp, refresh_token)
                return resp
        return {"message": "Username and password combination did not match any records"}, 401
