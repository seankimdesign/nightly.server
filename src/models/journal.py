from db import db


class JournalModel(db.Model):
    __tablename__ = 'journals'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    date = db.Column(db.String(10), primary_key=True)
    content = db.Column(db.Text)
    private = db.Column(db.Boolean)

    def __init__(self, user_id, date, content, private=False):
        self.user_id = user_id
        self.date = date
        self.content = content
        self.private = private

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "date": self.date,
            "content": self.content,
            "private": self.private
        }

    @classmethod
    def retrieve_by_user_id(cls, user_id):
        if user_id:
            return cls.query.filter_by(user_id=user_id).all()