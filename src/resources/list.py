from flask import request
from flask_restful import Resource

from models.journal import JournalModel


class List(Resource):

    def get(self, username=None):
        print(request.args)
        if username:
            return {"message": "Username given: {}".format(username)}
        return {"message": "No username given"}
