from flask import request
from flask_restful import Resource
from models.user import User
import json


class Register(Resource):

    # TODO: Implement db-synchronized id incrementor
    temp_id = 1

    def post(self):
        user_data = json.loads(request.data)
        new_user = User(Register.temp_id, **user_data)
        new_user.save_to_db()
        Register.temp_id += 1
        return {"message": "User saved"}

