from flask import request
from flask_restful import Resource

from models.user import UserModel


class Register(Resource):

    def post(self):
        user_json = request.json
        if not UserModel.is_valid_payload(user_json):
            return {"message": "Invalid request"}, 400
        user = UserModel.retrieve_by_username(user_json.get("username"))
        if user:
            return {"message": "Username already exists"}, 400
        user = UserModel.retrieve_by_email(user_json.get("email"))
        if user:
            return {"message": "Email already exists"}, 400
        new_user = UserModel(**user_json)
        try:
            new_user.save_to_db()
        except Exception:
            return {"message": "Service error, please try again"}, 500
        return {"message": "User record for {} saved".format(new_user.username)}, 201
