from flask import request
from flask_restful import Resource

from models.user import UserModel
from models.journal import JournalModel


class Post(Resource):

    def post(self):
        journal_json = request.json
        if not JournalModel.is_valid_payload(journal_json):
            return {"message": "Invalid request"}, 400
        user = UserModel.retrieve_by_username(journal_json.get('username'))
        if user is None:
            return {"message": "Invalid request"}, 400
        existing_post = JournalModel.retrieve_exact_post(username=journal_json['username'], date=journal_json['date'])
        if existing_post:
            existing_post.content = journal_json['content']
            existing_post.private = journal_json['private']
            current_post = existing_post
        else:
            current_post = JournalModel(**journal_json)
        if not current_post.is_editable():
            return {"message": "Post is archived and may not be modified"}, 400
        print('-----')
        try:
            print(current_post.to_dict())
            current_post.save_to_db()
        except Exception:
            return {"message": "Service error, please try again"}, 500
        return {"message": "Journal record for {} saved".format(user.username)}, 201
