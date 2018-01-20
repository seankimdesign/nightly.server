from flask import request
from flask_restful import Resource

from models.journal import JournalModel


class List(Resource):

    def get(self, username):
        n = request.args.get('n')
        d = request.args.get('d')
        try:
            n = int(n) if n else None
            d = int(d) if d else None
        except ValueError:
            return {"message": "Invalid request"}, 400
        entries = JournalModel.retrieve_by_username(username, count=n, daterange=d)
        print(entries)
        return List.format_response(entries, username, count=n, daterange=d)


    @classmethod
    def format_response(cls, entries, target, count=None, daterange=None):
        if entries and len(entries) > 0:
            entries_obj = {
                "entries": [entry.to_dict() for entry in entries]
            }
            query_obj = {
                "target": target,
                "matching": len(entries)
            }
            if count is not None:
                query_obj['count'] = count
            elif daterange:
                query_obj['range'] = daterange
            return {
                "query": query_obj,
                "entries": entries_obj
            }
