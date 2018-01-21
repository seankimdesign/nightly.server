import datetime

from db import db


class JournalModel(db.Model):
    __tablename__ = 'journals'

    username = db.Column(db.Integer, db.ForeignKey('users.username'), primary_key=True)
    date = db.Column(db.String(10), primary_key=True)
    content = db.Column(db.Text)
    private = db.Column(db.Boolean)

    def __init__(self, username, date, content, private=False):
        self.username = username
        self.date = str(date)
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

    def __lt__(self, other):
        return other.date < self.date

    @classmethod
    def retrieve_by_username(cls, username, count=None, daterange=10):
        if username:
            user_query = cls.query.filter_by(username=username)
            date_descending = cls.date.desc()
            if count == 0:
                return user_query.order_by(date_descending).all()
            elif count:
                return user_query.order_by(date_descending).limit(count).all()
            else:
                start_date = str(datetime.date.today() - datetime.timedelta(daterange))
                return user_query.filter(cls.date >= start_date).order_by(date_descending).all()

    @classmethod
    def convert_date(cls, date_string):
        if type(date_string) is datetime.date:
            return date_string
        datelist = date_string.split('-')
        if len(datelist) == 3:
            return datetime.date(*[int(dateunit) for dateunit in datelist])
        raise ValueError('Invalid date string provided')
