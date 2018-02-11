from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources.register import Register
from resources.login import Login
from resources.list import List
from resources.post import Post
from authorization import initialize_jwt, jwt_configs

# Establish JournalModel class definition prior to `users` table instantiation
from models.journal import JournalModel

app = Flask(__name__)

# TODO: Move into configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# TODO: Move into configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

for key, value in jwt_configs.items():
    app.config[key] = value

# TODO: Move into configuration
cors = CORS(app, origins="http://localhost:7777")
api = Api(app)
jwt = JWTManager(app)
initialize_jwt(jwt)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Register, '/register')
api.add_resource(Login, '/login/<string:username>')
api.add_resource(List, '/list/<string:username>')
api.add_resource(Post, '/post')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
