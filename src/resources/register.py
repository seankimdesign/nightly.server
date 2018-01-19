from flask import request
from flask_restful import Resource
from models.user import UserModel


class Register(Resource):

    def post(self):
        user_json = request.json
        try:
            new_user = UserModel(**user_json)
            new_user.save_to_db()
        except TypeError:
            return {"message": "Invalid request"}, 400
        except Exception:
            return {"message": "Service error, please try again"}, 500
        return {"message": "User record for {} saved".format(new_user.username)}, 201
