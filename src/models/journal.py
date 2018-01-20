from db import db


class JournalModel(db.Model):
    __tablename__ = 'journals'

    username = db.Column(db.Integer, db.ForeignKey('users.username'), primary_key=True)
    date = db.Column(db.String(10), primary_key=True)
    content = db.Column(db.Text)
    private = db.Column(db.Boolean)

    def __init__(self, username, date, content, private=False):
        self.username = username
        self.date = date
        self.content = content
        self.private = private

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "username": self.username,
            "date": self.date,
            "content": self.content,
            "private": self.private
        }

    @classmethod
    def retrieve_by_username(cls, username, count=None, daterange=10):
        if username:
            print(count)
            if count == 0:
                return cls.query.filter_by(username=username).all()
            elif count:
                return cls.query.filter_by(username=username).limit(count).all()
            else:
                pass
