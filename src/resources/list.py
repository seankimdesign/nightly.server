from flask_restful import Resource

from models.journal import JournalModel


class List(Resource):

    def get(self, username=None):
        if username:
            return {"message": "Username given: {}".format(username)}
        return {"message": "No username given"}
