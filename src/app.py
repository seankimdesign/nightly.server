from flask import Flask
from flask_restful import Api
from resources.register import Register
from resources.login import Login

app = Flask(__name__)

# TODO: Move into configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Register, '/register')
api.add_resource(Login, '/login/<string:username>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
